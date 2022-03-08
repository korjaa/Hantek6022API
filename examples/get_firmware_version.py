#!/usr/bin/python3

__author__ = 'Robert Cope'
"""
"""

from PyHT6022.LibUsbScope import Oscilloscope

scope = Oscilloscope()
scope.setup()
version = scope.get_fw_version()
if version:
    print( hex( version ) )
