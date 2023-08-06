import fcntl
import struct
import termios

from .alerts import debug

def terminal_size(fd=0):
    """Return `columns, rows`; `None, None` if not supported by device."""
    try:
        packed_args = struct.pack('HHHH', 0, 0, 0, 0)
        packed_result = fcntl.ioctl(fd, termios.TIOCGWINSZ, packed_args)
        rows, cols, *_ = struct.unpack('HHHH', packed_result)
        return cols, rows
    except OSError:
        return None, None

ttyo_file = None
ttyi_file = None

def ttyo(close=False):
    global ttyo_file
    if close:
        if ttyo_file:
            ttyo_file.close()
            ttyo_file = None
        return
    if not ttyo_file:
        ttyo_file = open("/dev/tty", "w")
    return ttyo_file

def ttyi(close=False):
    global ttyi_file
    if close:
        if ttyi_file:
            ttyi_file.close()
            ttyi_file = None
        return
    if not ttyi_file:
        ttyi_file = open("/dev/tty")
    return ttyi_file

def ptty(*args, **kwargs):
    print(*args, file=ttyo(), **kwargs)

# EOF
