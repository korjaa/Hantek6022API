#!/usr/bin/python3

__author__ = 'Jochen Hoenicke'

import sys
from PyHT6022.LibUsbScope import Oscilloscope

scope = Oscilloscope()
scope.setup()
if not scope.open_handle():
    sys.exit( -1 )

calibration = scope.get_calibration_values( 48 )
scope.close_handle()
# print( calibration )
for x in calibration:
    print( hex(x), end=" " )
