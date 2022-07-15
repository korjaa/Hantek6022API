#!/usr/bin/python3

# flash the firmware from hex file

import sys
from PyHT6022.LibUsbScope import Oscilloscope

if len( sys.argv ) > 1:
    firmware = sys.argv[ 1 ]
    scope = Oscilloscope()
    scope.setup()
    if not scope.open_handle():
        sys.exit( -1 )
    scope.flash_firmware_from_hex( firmware )
    print( "FW version", hex( scope.get_fw_version() ) )
    scope.close_handle()
else:
    print( "usage: " + sys.argv[0] + " path_to_hexfile" )
