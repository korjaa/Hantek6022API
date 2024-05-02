#!/usr/bin/python3

'''
Simple demo program that reads the output of 'capture_6022.py'
and creates the amplitude spectrum plots of both channels.
It uses the extra python package 'matplotlib' for visualisation.
Install with: 'apt install python3-matplotlib' if missing.
'''

import csv
import matplotlib.pyplot as plt
import sys
import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser(
    prog='fft_from_capture_6022.py',
    description='Plot FFT of output from capture_6022.py, use hann windowing' )
ap.add_argument( '-i', '--infile', type = argparse.FileType('r'),
    help='read the data from INFILE, (default: stdin)' )
ap.add_argument( '-x', '--xkcd', action = 'store_true',
    help='plot in XKCD style :)' )
options = ap.parse_args()

if options.xkcd:
    plt.xkcd()

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

# Sample frequency
fs = 1 / ( time[1] - time[0] )

# Stack plots in two rows, one column, sync their frequency axes
fig, axs = plt.subplots( 2, 1, sharex = True )

# Channel 1 spectrum (default window: hanning)
axs[0].magnitude_spectrum( ch1, fs, scale = 'dB' )
axs[0].grid( True )

# Channel 2 spectrum (default window: hanning)
axs[1].magnitude_spectrum( ch2, fs, scale = 'dB' )
axs[1].grid( True )

# And display everything
plt.show()
