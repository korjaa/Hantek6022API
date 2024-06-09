#!/usr/bin/python3

import sys
from Hantek6022B import Hantek6022B

scope = Hantek6022B()
scope.setup()
if not scope.open_handle():
    sys.exit( -1 )

eeprom = scope.read_eeprom( 0, 256 )
scope.close_handle()

f = open( "eeprom_256.dat", "wb" )
f.write( eeprom )
f.close()

print( eeprom )
