#!/usr/bin/python3

'''
Simple demo program that reads the output of 'capture_6022.py'
and plots the signal and spectrum of one or both channels.
It uses the extra python package 'matplotlib' for visualisation.
Install with: 'apt install python3-matplotlib' if missing.
'''

import csv
import matplotlib.pyplot as plt
import matplotlib.mlab as ml
import sys
import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser(
    prog='plot_from_capture_6022.py',
    description='Plot output of capture_6022.py over time' )
ap.add_argument( '-i', '--infile', type = argparse.FileType('r'),
    help='read the data from INFILE (default: use stdin)' )
ap.add_argument( '-c', '--channel', type = int, default = 0,
    help='show only CH1 or CH2, default: show both)' )
ap.add_argument( '-s', '--spectrum',
    dest = 'max_freq',
    const = -1,
    default = 0,
    action = 'store',
    nargs = '?',
    type = int,
    help = 'display the spectrum of the samples, optional up to MAX_FREQ' )
ap.add_argument( '-x', '--xkcd', action = 'store_true',
    help='plot in XKCD style :)' )
options = ap.parse_args()

if options.channel not in (0, 1, 2):
    print( 'error, channel must be 1 or 2' )
    sys.exit()

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
    ch1.append( float( row[1] ) )
    ch2.append( float( row[2] ) )

infile.close()

# calculate sample frequency
fs = ( len( time ) - 1 ) / ( time[-1] - time[0] )

if options.channel == 0:
# Stack plots in two rows, one or two columns, sync their time and frequency axes
    if options.max_freq:
        fig, ( (v1, sp1), (v2, sp2) ) = plt.subplots( 2, 2, sharex = 'col' )
        # Channel 1 spectrum
        sp1.set_title( 'Spectrum 1' )
        sp1.magnitude_spectrum( ch1, fs, scale = 'dB', color = 'C1' )
        if options.max_freq > 0:
            sp1.axes.set_xlim( [ 0, options.max_freq ] )
        sp1.grid( True )
        # Channel 2 spectrum
        sp2.set_title( 'Spectrum 2' )
        sp2.magnitude_spectrum( ch2, fs, scale = 'dB', color = 'C0' )
        if options.max_freq > 0:
            sp1.axes.set_xlim( [ 0, options.max_freq ] )
        sp2.grid( True )

    else:
        fig, ( v1, v2 ) = plt.subplots( 2, 1, sharex = 'col' )

    # Channel 1 data
    v1.set_title( 'Channel 1' )
    v1.plot( time, ch1, color = 'C1' )
    v1.set(xlabel='Time', ylabel='Voltage (V)' )
    v1.grid( True )
    # Channel 2 data
    v2.set_title( 'Channel 2' )
    v2.plot( time, ch2 )
    v2.set(xlabel='Time', ylabel='Voltage (V)' )
    v2.grid( True )

else: # CH1 or CH2
    if options.channel == 1:
        ch = ch1
        color = 'C1'
    else:
        ch = ch2
        color = 'C0'
# Plot in one rows, one or two columns
    if options.max_freq:
        fig, ( v, sp ) = plt.subplots( 1, 2 )
        # Channel 1 spectrum
        sp.set_title( 'Spectrum ' + str( options.channel ) )
        sp.magnitude_spectrum( ch, fs, scale = 'dB', color = color )
        if options.max_freq > 0:
            sp.axes.set_xlim( [ 0, options.max_freq ] )
        sp.grid( True )
    else:
        fig, v = plt.subplots( 1 )

    # Channel data
    v.set_title( 'Channel ' + str( options.channel ) )
    v.plot( time, ch, color = color )
    v.set(xlabel='Time', ylabel='Voltage (V)' )
    v.grid( True )


fig.tight_layout()
# fig.savefig('test.jpg')
# And display everything
plt.show()
