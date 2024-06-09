#!/usr/bin/python3

__author__ = 'Robert Cope'

import sys
from Hantek6022B import Hantek6022B
from Hantek6022B.Firmware import firmware as Firmware

scope = Hantek6022B()
scope.setup()
if not scope.open_handle():
    sys.exit( -1 )

scope.flash_firmware( firmware = Firmware )
print( "FW version", hex( scope.get_fw_version() ) )
scope.close_handle()
