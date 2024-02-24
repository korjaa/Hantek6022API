#!/usr/bin/python3

# flash the file "firmware_BL.hex" on the DSO6022BE
# this device has the same HW as DSO6022, but different PID=0x2020
# it will become a DSO6022 when the FW is loaded
import sys
from PyHT6022.LibUsbScope import Oscilloscope

firmware = "dso6022bl-firmware.hex"
VID=0x04b4
PID=0x6022

scope = Oscilloscope( VID, PID )
scope.setup()
if not scope.open_handle():
    sys.exit( -1 )
scope.flash_firmware_from_hex( firmware )
print( "Product", scope.get_product_string() )
print( "FW version", hex( scope.get_fw_version() ) )
scope.close_handle()
