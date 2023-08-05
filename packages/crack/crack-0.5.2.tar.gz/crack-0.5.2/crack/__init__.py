# -*- coding: utf-8 -*-
# @author: leesoar

"""crack"""

import sys

from crack.util import *
try:
    from pysodium import *
except ValueError:
    # if error -> need install libsodium
    pass


__version__ = "0.5.2"

if sys.version_info >= (3, 6):
    from secrets import *