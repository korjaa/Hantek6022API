#!/usr/bin/python3

from PyHT6022.LibUsbScope import Oscilloscope

scope = Oscilloscope()
scope.setup()
scope.open_handle()
scope.flash_firmware()
print( "FW version", hex( scope.get_fw_version() ) )

# read 1st 8 bytes
eeprom = scope.read_eeprom( 0, 8 )
print( eeprom )

#EE_SIZE = 128 # 16 KByte 24C128
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
hantek6022_id = (f.read())
f.close()

print( hantek6022_id )

# write new content
scope.write_eeprom( 0, hantek6022_id )
scope.close_handle()


