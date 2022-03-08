#!/usr/bin/python3

import sys
from PyHT6022.LibUsbScope import Oscilloscope

scope = Oscilloscope()
scope.setup()
if not scope.open_handle():
    sys.exit( -1 )

scope.flash_firmware()
print( "FW version", hex( scope.get_fw_version() ) )

# read 1st 8 bytes
eeprom = scope.read_eeprom( 0, 8 )
# print( eeprom )

# EE_SIZE = 128 # 16 KByte 24C128
EE_SIZE = 2 # 256 Byte 24C02

# clear eeprom
empty = bytearray( 128 )
adr = 0
while adr < EE_SIZE * 128:
	print( "Erase", hex(adr) )
	scope.write_eeprom( adr, empty )
	adr += 128

# get the Hantek6022BE id
f = open( "eeprom_6022.dat", "rb" )
hantek_id = (f.read())
f.close()

for b in hantek_id:
	print( hex( b ), end=' ' )
print()

# write new content
scope.write_eeprom( 0, hantek_id )
scope.close_handle()

