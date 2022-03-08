#!/usr/bin/python3

__author__ = 'Robert Cope'

import sys
from PyHT6022.LibUsbScope import Oscilloscope
from PyHT6022.Firmware import mod_firmware_01 as Firmware

scope = Oscilloscope()
scope.setup()
if not scope.open_handle():
    sys.exit( -1 )
scope.flash_firmware( firmware = Firmware )
scope.close_handle()
