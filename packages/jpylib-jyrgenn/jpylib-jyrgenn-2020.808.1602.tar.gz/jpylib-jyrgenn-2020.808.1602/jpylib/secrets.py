#!/usr/bin/env python3

import os
import sys
import zlib
import fcntl
import base64
import shutil
import collections
from datetime import datetime

from .alerts import *

# Where to look for the secrets file.
basedir = "/" if os.geteuid() == 0 else os.environ.get('HOME')
default_filename = os.path.join(basedir, "etc/secrets")

# suffix of backup file
backup_suffix = ".backup"

# prefix of end line
end_prefix = "# written by putsecret() "

# Default character encoding to use; this *should* depend on the environment,
# but I am too lazy to do that now.
default_char_encoding = "utf-8"

# En- and decoder functions. The names must be {en,de}code_{tag}, so they can be
# found in globals().

def encode_b64(data):
    """Encode data in base64."""
    return base64.b64encode(data)

def decode_b64(data):
    """Decode base64-encoded data."""
    return base64.b64decode(data)

def decode_zip(data):
    """Decode a zipped string. Implies base64 encoding of zip data."""
    zipped = decode_b64(data)
    return zlib.decompress(zipped)

def encode_zip(data):
    """Zip-compress data. Implies base64 encoding of zip data."""
    zipped = zlib.compress(data)
    return encode_b64(zipped)

valid_options = set([
    name[7:] for name in globals().keys()
    if name.startswith("encode_") or name.startswith("decode_") ])

# encode/decode direction
dir_encode = 0
dir_decode = 1
de_en_prefix = ["encode_", "decode_"]


class OptionUnknownError(LookupError):
    """An exception indicating that a corresponding option was not found."""
    pass

    
def find_coder_func(option, direction, must_find=False):
    coder_name = de_en_prefix[direction] + option
    coder_func = globals().get(coder_name)
    if coder_func or not must_find:
        return coder_func
    else:
        raise OptionNotFoundError("encountered unknown option", option)


def maybe_decode(options, value, char_encoding):
    """Decode the found value, if options are present.

    `options`        array of options
    `value`          the value to decode
    `char_encoding`  the bytes => string encoding to use.
    """
    for opt in options:
        coder_func = find_coder_func(opt, dir_decode)
        if coder_func:
            data = coder_func(bytes(value, char_encoding))
            value = str(data, char_encoding)
        else:
            notice("secrets: found unknown encoding '{}'".format(opt))
    return value


def read_secrets(fname, get_invalids=False):
    """Read in a secrets file and return its entries.

    Return an ordered dictionary with entries key:([opts], value). If the key is
    a comment line or otherwise not a valid key:value or key:opts:value line,
    opts and value are None, or if get_invalids is false (the default), it is
    not included at all.

    Otherwise, opts is a list of options, which may be empty.

    If there are two colons in a line and the field between the colons is not
    empty, but contains no valid options, the line is treated as a key:value
    line.

    """
    entries = collections.OrderedDict()
    with open(fname) as f:
        for line in f:
            line = line.rstrip()
            if line.lstrip().startswith("#"):
                # a comment line
                if line.startswith(end_prefix):
                    # the "written by putsecret()" line, skip it
                    continue
                if get_invalids:
                    entries[line] = (None, None)
                continue
            # non-commented lines
            fields = line.split(":", 2)
            nfields = len(fields)
            assert 1 <= nfields <= 3, "unexpected # of fields: "+str(nfields)
            if nfields == 1:
                # not a key:[opts:]value line
                if get_invalids:
                    entries[line] = (None, None)
                continue
            key = fields[0]
            if key in entries:
                info("secrets: ignore duplicate entry for '{}'".format(tag))
                continue
            if nfields == 2:
                # key:value
                entries[key] = ([], fields[1])
                continue
            if nfields == 3:
                # key:[opts]:value
                if fields[1] == "":
                    # key::value
                    entries[key] = ([], fields[2])
                    continue
                opts = fields[1].split(",")
                if all([ opt in valid_options for opt in opts ]):
                    # valid options
                    entries[key] = (opts, fields[2])
                else:
                    # non-valid options field, so it's key:value again
                    entries[key] = ([], ":".join(fields[1:]))
    return entries

def putsecret(key, value, fname=None, options=None,
              char_encoding=default_char_encoding):
    """Put a secret tagged with `key` into the secrets file `fname`.

    A backup copy is made as {fname}.backup. A temporary file named
    .../.{basename}.newtmp is created, which also serves as a lockfile. After
    all records are written to the temporary file, it is moved into place,
    deleting the original secrets file.

    """
    def write_line(key, opts=None, value=None):
        if opts is None:
            line = key
        else:
            line = ":".join([key, ",".join(opts), value])
        print(line, file=out)
    
    fname = fname or default_filename
    entries = collections.OrderedDict()
    shutil.copy2(fname, fname + backup_suffix)

    options = options or []
    for opt in options:
        data = bytes(value, char_encoding)
        data = find_coder_func(opt, dir_encode, must_find=True)(data)
        value = str(data, char_encoding)
    newfile = os.path.join(os.path.dirname(fname),
                           "." + os.path.basename(fname) + ".newtmp")
    try:
        with open(newfile, "x") as out:
            os.chmod(newfile, 0o600)
            # now, read in entries, change/set new one, write out again
            entries = read_secrets(fname, get_invalids=True)
            entries[key] = (options, value)
            for key, data in entries.items():
                options, value = data
                if options is not None:
                    write_line(key, options, value)
                else:
                    write_line(key)
            write_line(end_prefix+datetime.now().isoformat(timespec="seconds"))
        os.rename(newfile, fname)
    except FileExistsError:
        raise FileExistsError("temp file {} exists, aborting" .format(newfile))
    finally:
        try:
            os.remove(newfile)
        except:
            pass


def getsecret(key, fname=None, char_encoding=None, error_exception=True):
    """Get a secret tagged with `key` from the secrets file `fname`.

    The default pathname for the secrets file is `/etc/secrets` if
    called by root, and `$HOME/etc/secrets` for normal users.

    The file consist of lines of the form `_key_:_value_`, so the key
    may not contain a colon. Whitespace is significant except at the end
    of the line, where it will be stripped, so the secret may not end
    with whitespace. You can get around these limitations by encoding
    key and/or value with e.g. base64.

    If the key is found, the value is returned. Otherwise, a `KeyError`
    exception is raised. The exception's arguments are a format string,
    the key, and the file name. (Splitting this up allows for subsequent
    i18n.)

    If the found value for the key starts with "{b64}", it will be
    base64-decoded before it is returned.

    """
    if fname is None:
        fname = default_filename
    try:
        os.chmod(fname, 0o600)
    except:
        pass
    
    data = read_secrets(fname).get(key)
    if data and data[0] is not None:
            return maybe_decode(*data, char_encoding or default_char_encoding)
    if bomb:
        raise KeyError("cannot find secret for '{}' in '{}'", key, fname)
    return None


def main():
    if not (2 <= len(sys.argv) <= 3):
        sys.exit("usage: getsecret key [filename]")
    try:
        print(getsecret(*sys.argv[1:]))
    except Exception as e:
        sys.exit("getsecret: " + e.args[0].format(*e.args[1:]))


if __name__ == '__main__':
    main()
