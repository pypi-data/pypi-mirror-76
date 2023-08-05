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

