#!/usr/bin/python3

__author__ = 'Jochen Hoenicke'

import sys
from PyHT6022.LibUsbScope import Oscilloscope


scope = Oscilloscope()
scope.setup()
if not scope.open_handle():
    sys.exit( -1 )

# read at end-16, 16 bytes
eeprom = scope.read_eeprom( 256 - 16, 16 )

# write at end-16
scope.write_eeprom( 256 - len( eeprom ), eeprom )
scope.close_handle()

print( eeprom )
