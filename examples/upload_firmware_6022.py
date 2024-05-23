#!/usr/bin/python3

"""
Flash firmware into device
either default firmware when called without arguments
depending on device VID/PID
or firmware-DSO6022BE or firmware-DSO6022BL with provided VID:PID
"""
import sys
from PyHT6022.LibUsbScope import Oscilloscope
from PyHT6022.Firmware import dso6022be_firmware, dso6022bl_firmware
import argparse

ap = argparse.ArgumentParser(
    prog='upload_firmware_6022.py',
    description='Upload firmware to Hantek6022 devices with different VID:PID' )
ap.add_argument( '-V', '--VID', type = lambda x: int(x,16), default = 0 )
ap.add_argument( '-P', '--PID', type = lambda x: int(x,16), default = 0 )
fw = ap.add_mutually_exclusive_group()
fw.add_argument( '--be', '--6022be', action = 'store_true' )
fw.add_argument( '--bl', '--6022bl', action = 'store_true' )

options = ap.parse_args()
print( options.VID, options.PID )
if not options.VID and not options.PID:
    scope = Oscilloscope()
elif options.VID and options.PID and ( options.be or options.bl ):
    scope = Oscilloscope(options.VID, options.PID)
else:
    print( '--VID and --PID and one of --be or --bl must be provided')
    sys.exit()

scope.setup()
if not scope.open_handle():
    print( 'No device' )
    sys.exit( -1 )

if options.be:
    scope.flash_firmware( dso6022be_firmware )
elif options.bl:
    scope.flash_firmware( dso6022bl_firmware )
else:
    scope.flash_firmware()

print( "FW version", hex( scope.get_fw_version() ) )
scope.close_handle()
