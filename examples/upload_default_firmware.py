#!/usr/bin/python3

__author__ = 'Robert Cope'

import sys
from PyHT6022.LibUsbScope import Oscilloscope
from PyHT6022.Firmware import firmware as Firmware

scope = Oscilloscope()
scope.setup()
if not scope.open_handle():
    sys.exit( -1 )

scope.flash_firmware( firmware = Firmware )
print( "FW version", hex( scope.get_fw_version() ) )
scope.close_handle()
