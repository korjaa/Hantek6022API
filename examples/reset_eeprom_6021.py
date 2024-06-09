#!/usr/bin/python3

'''
DANGER!
This tool erases the complete EEPROM and restores only the data for the "C0 Load"

At power-on reset, if the FX2LP device detects an EEPROM connected to its I2C bus
with the value 0xC0 at address 0, EZ-USB automatically copies the VID, PID, and DID
from the EEPROM into internal storage. The table shows the data format for a C0 Load.

----------------------------------
| EEPROM  |                      |
| Address |       Contents       |
---------------------------------|
|   0     |  0xC0                |
|   1     |  Vendor ID  (VID) L  |
|   2     |  Vendor ID  (VID) H  |
|   3     |  Product ID (PID) L  |
|   4     |  Product ID (PID) H  |
|   5     |  Device ID  (DID) L  |
|   6     |  Device ID  (DID) H  |
|   7     |  Configuration Byte  |
----------------------------------
'''


import sys
from Hantek6022B import Hantek6022B


def hexdump( txt, bytes ):
    print( txt, end=': ' )
    for b in bytes:
        print( hex( b ), end=' ' )
    print()



print( 'WARNING: this will erase all calibration data in EEPROM, proceed? [y/N]', end = ' ' )
yes_no = input()


if yes_no == '' or yes_no[0].lower() != 'y':
    print( 'Aborted' )
    sys.exit()


scope = Hantek6022B()
scope.setup()
if not scope.open_handle():
    print( 'Error opening the scope device' )
    sys.exit( -1 )

scope.flash_firmware()
print( 'FW version', hex( scope.get_fw_version() ) )

id_file = 'eeprom_6021.dat'

# get the Hantek6021 id
try:
    f = open( id_file, 'rb' )
except FileNotFoundError:
    print( 'Error opening', id_file )
else:
    with f:
        new_id = f.read()

        # read 1st 8 bytes
        eeprom = scope.read_eeprom( 0, 8 )
        hexdump( 'EEPROM', eeprom )

        # EE_SIZE = 64 # 16 KByte 24C128
        EE_SIZE = 1 # 256 Byte 24C02

        # clear eeprom
        empty = bytearray( 256 )
        adr = 0
        while adr < EE_SIZE * 256:
            print( 'Erase address', hex(adr) )
            scope.write_eeprom( adr, empty )
            adr += 256
        # store id
        hexdump( 'Store Hantek DSO-6021 id', new_id )
        scope.write_eeprom( 0, new_id )

finally:
    scope.close_handle()
