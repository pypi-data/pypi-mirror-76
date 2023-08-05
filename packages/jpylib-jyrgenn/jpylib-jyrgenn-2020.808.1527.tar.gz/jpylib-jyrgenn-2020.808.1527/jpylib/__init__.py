#!/usr/bin/env python3
# Have all support function modules here at hand.

import os
import pwd
import sys

from .pgetopt import parse as pgetopts
from .alerts import L_ERROR, L_NOTICE, L_INFO, L_DEBUG, L_TRACE, \
    alert_config, alert_level, alert_level_name, \
    alert_level_up, alert_level_zero, is_notice, is_info, is_debug, is_trace, \
    debug_vars, fatal, err, notice, info, debug, trace
from .fntrace import tracefn
from .stringreader import StringReader
from .kvs import parse_kvs
from .namespace import Namespace
from .config import Config
from .secrets import getsecret
from .secrets import main as getsecret_main
from .secrets import putsecret
from .sighandler import sanesighandler
from .terminal import terminal_size
from .capture import outputCaptured, outputAndExitCaptured
from .process import backquote
from .assorted import boolish

version = "2020.808.1527"
program = os.path.basename(sys.argv[0])
real_home = pwd.getpwuid(os.getuid()).pw_dir
home = os.environ.get("HOME") or real_home

def ttyo(close=False):
    if close:
        if getattr(ttyo, "file", None):
            ttyo.file.close()
            ttyo.file = None
        return
    if not getattr(ttyo, "file", None):
        ttyo.file = open("/dev/tty", "w")
    return ttyo.file

def ttyi(close=False):
    if close:
        if getattr(ttyi, "file", None):
            ttyi.file.close()
            ttyi.file = None
        return
    if not getattr(ttyi, "file", None):
        ttyi.file = open("/dev/tty")
    return ttyi.file

def ptty(*args, **kwargs):
    print(*args, file=ttyo(), **kwargs)
