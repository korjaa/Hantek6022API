#!/usr/bin/python3


from PyHT6022.LibUsbScope import Oscilloscope
import sys

usage = 'usage: set_cal_out_freq_6022 FREQ\nwith 32 <= FREQ <= 100000'

if len( sys.argv ) < 2:
    print( usage, file=sys.stderr )
    sys.exit( -1 )
cal_freq = int( sys.argv[1])

if cal_freq < 32 or cal_freq > 100000:
    print( usage, file=sys.stderr )
    sys.exit( -1 )

scope = Oscilloscope()
scope.setup()

if not scope.open_handle():
    sys.exit( -1 )

# upload correct firmware into device's RAM
if (not scope.is_device_firmware_present):
    scope.flash_firmware()

if not scope.set_calibration_frequency( cal_freq ):
    print( 'error', file=sys.stderr )
