#!/usr/bin/python3


from PyHT6022.LibUsbScope import Oscilloscope
import sys
'''set the frequency of calibration output from 1st command line argument.
frequency must be '''

usage = 'usage: set_cal_out_freq_6022 FREQ\nwith 32 <= FREQ <= 100000'

if len( sys.argv ) < 2:
    print( usage, file=sys.stderr )
    sys.exit()
cal_freq = int( sys.argv[1])

if cal_freq < 32 or cal_freq > 100000:
    print( usage, file=sys.stderr )
    sys.exit()

scope = Oscilloscope()
scope.setup()
scope.open_handle()

if not scope.set_calibration_frequency( cal_freq ):
    print( 'error', file=sys.stderr )

