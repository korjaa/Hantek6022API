#!/usr/bin/python3

__author__ = 'Jochen Hoenicke'

import sys
from PyHT6022.LibUsbScope import Oscilloscope

scope = Oscilloscope()
scope.setup()
if not scope.open_handle():
    sys.exit( -1 )

eeprom = scope.read_eeprom(0, 8)
scope.close_handle()

f = open( "eeprom.dat", "wb" )
f.write( eeprom )
f.close()

print( eeprom )
