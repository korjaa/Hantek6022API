#!/usr/bin/python3

import sys
from Hantek6022B import Hantek6022B

firmware = "dso6021-firmware.hex"
VID=0x04b4
PID=0x6021

scope = Hantek6022B( VID, PID )
scope.setup()
if not scope.open_handle():
    sys.exit( -1 )
scope.flash_firmware_from_hex( firmware )
print( "FW version", hex( scope.get_fw_version() ) )
scope.close_handle()
