#!/usr/bin/python3

__author__ = 'Robert Cope'

from PyHT6022.LibUsbScope import Oscilloscope
from PyHT6022.Firmware import firmware as Firmware

scope = Oscilloscope()
scope.setup()
scope.open_handle()
scope.flash_firmware( firmware = Firmware )
print( "FW version", hex( scope.get_fw_version() ) )
scope.close_handle()
