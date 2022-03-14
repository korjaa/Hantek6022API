#!/usr/bin/python3

import sys
from PyHT6022.LibUsbScope import Oscilloscope

scope = Oscilloscope()
scope.setup()
if not scope.open_handle():
    sys.exit( -1 )

# read eeprom content from file
f = open( "eeprom_256.dat", "rb" )
eeprom = f.read()
f.close()

# write_eeprom content
scope.write_eeprom( len( eeprom ), eeprom )
scope.close_handle()

print( eeprom )
