#!/usr/bin/python3

'''
Simple demo program that reads the output of 'capture_6022.py'
and creates the amplitude spectrum plots of both channels.
It uses the extra python package 'matplotlib' for visualisation.
Install with: 'apt install python3-matplotlib' if missing.
'''

import csv
import math
import matplotlib.mlab as ml
import matplotlib.pyplot as plt
import numpy as np
import sys
import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser(
    prog='fft_from_capture_6022.py',
    description='Plot FFT of output from capture_6022.py, use hann windowing as default' )
ap.add_argument( '-i', '--infile', type = argparse.FileType('r'),
    help='read the data from INFILE, (default: stdin)' )
windows = ap.add_mutually_exclusive_group()
windows.add_argument( '-f', '--flat_top', action = 'store_true',
                     help='use flat top window')
windows.add_argument( '-n', '--no_window', action = 'store_true',
                     help='use no window')
ap.add_argument( '-x', '--xkcd', action = 'store_true',
    help='plot in XKCD style :)' )
options = ap.parse_args()

infile = options.infile or sys.stdin

# Use output of 'capture_6022.py'
# Format: no header, values are SI units s and V, separated by comma
# The data amount should be limited to a few seconds e.g. with '-t2'

# process the csv data
capture = csv.reader( infile )

# separate into three lists
time, ch1, ch2 = [], [], []
for row in capture:
    time.append( float( row[0] ) )
    # scale to dbV:
    # multiply by 2 because we use only half of the spectrum ...
    # ... then divide by sqrt(2) to scale to rms -> * sqrt(2)
    ch1.append( float( row[1] ) * 1.4142 )
    ch2.append( float( row[2] ) * 1.4142 )

infile.close()


##############################
# define own window function #
##############################
#
def flat_top( x ):
    N = len( x )
    # use matlab coefficients -> https://www.mathworks.com/help/signal/ref/flattopwin.html
    # scaled by 1/0.21547095 to get an overall window amplitude gain of 1.0
    a0, a1, a2, a3, a4 = 1, 1.933732403, 1.286777443, 0.387889630, 0.032242713
    p = 2 * math.pi / (N-1)
    # gain = 0
    for n in range( N ):
        x[n] = (
            a0
          - a1 * math.cos( p * n )
          + a2 * math.cos( p * n * 2 )
          - a3 * math.cos( p * n * 3 )
          + a4 * math.cos( p * n * 4 )
        )
        # gain += x[n]
    # print( "flat_top:", gain/N )
    return x
#
##############################


if options.flat_top:
    window = flat_top
elif options.no_window:
    window = ml.window_none
else:
    window = None # default: hann window

# Sample frequency
fs = 1 / ( time[1] - time[0] )

if options.xkcd:
    plt.xkcd()

# Stack plots in two rows, one column, sync their frequency axes
fig, axs = plt.subplots( 2, 1, sharex = True )

# Channel 1 spectrum
axs[0].magnitude_spectrum( ch1, fs, scale = 'dB', window = window )
axs[0].grid( True )
axs[0].set_title( 'Spectrum 1')

# Channel 2 spectrum
axs[1].magnitude_spectrum( ch2, fs, scale = 'dB', window = window )
axs[1].grid( True )
axs[1].set_title( 'Spectrum 2')

fig.tight_layout()
# And display everything
plt.show()
