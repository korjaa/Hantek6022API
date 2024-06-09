#!/usr/bin/python3

"""
Flash default firmware into device
either firmare-DSO6022BE or firmware-DSO6022BL or firmware-DSO6021
depending on VID/PID
"""
import sys
from Hantek6022B import Hantek6022B

scope = Hantek6022B()
scope.setup()
if not scope.open_handle():
    sys.exit( -1 )
scope.flash_firmware()
print( "FW version", hex( scope.get_fw_version() ) )
scope.close_handle()
