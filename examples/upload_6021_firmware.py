#!/usr/bin/python3

from PyHT6022.LibUsbScope import Oscilloscope

firmware = "dso6021-firmware.hex"
VID=0x04b4
PID=0x6021

scope = Oscilloscope( VID, PID )
scope.setup()
scope.open_handle()
scope.flash_firmware_from_hex( firmware )
print( "FW version", hex( scope.get_fw_version() ) )
scope.close_handle()
