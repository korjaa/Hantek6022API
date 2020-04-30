#!/usr/bin/python3

# flash the file "firmware_BE.hex" on the DSO2020 
# this device has the same HW as DSO6022, but different PID=0x2020
# it will become a DSO6022 when the FW is loaded

from PyHT6022.LibUsbScope import Oscilloscope

firmware = "dso6022be_firmware.hex"
VID=0x04b4
PID=0x2020

scope = Oscilloscope( VID, PID )
scope.setup()
scope.open_handle()
scope.flash_firmware_from_hex( firmware )
print( "FW version", hex( scope.get_fw_version() ) )
scope.close_handle()
