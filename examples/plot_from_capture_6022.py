#!/usr/bin/python3

'''
Simple demo program that reads the output of 'capture_6022.py'
and plots the signal and spectrum of one or both channels.
It uses the extra python package 'matplotlib' for visualisation.
Install with: 'apt install python3-matplotlib' if missing.
'''

import csv
import math
import matplotlib.pyplot as plt
import matplotlib.mlab as ml
import sys
import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser(
    prog='plot_from_capture_6022.py',
    description='Plot output of capture_6022.py (and optional spectrum) over time' )
ap.add_argument( '-i', '--infile', type = argparse.FileType('r'),
    help='read the data from INFILE (default: stdin)' )
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
windows = ap.add_mutually_exclusive_group()
windows.add_argument( '-f', '--flat_top', action = 'store_true',
                     help='use flat top window for fft')
windows.add_argument( '-n', '--no_window', action = 'store_true',
                     help='use no window for fft')
ap.add_argument( '-x', '--xkcd', action = 'store_true',
    help='plot in XKCD style :)' )
options = ap.parse_args()

if options.channel not in (0, 1, 2):
    print( 'error, channel must be 1 or 2' )
    sys.exit()

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
    window = None # default: hanning window

# calculate sample frequency
fs = ( len( time ) - 1 ) / ( time[-1] - time[0] )

if options.xkcd:
    plt.xkcd()

if options.channel == 0:
# Stack plots in two rows, one or two columns, sync their time and frequency axes
    if options.max_freq:
        fig, ( (v1, sp1), (v2, sp2) ) = plt.subplots( 2, 2, sharex = 'col' )
        # Channel 1 spectrum
        sp1.set_title( 'Spectrum 1' )
        sp1.magnitude_spectrum( ch1, fs, scale = 'dB', color = 'C1', window = window )
        if options.max_freq > 0:
            sp1.axes.set_xlim( [ 0, options.max_freq ] )
        sp1.grid( True )
        # Channel 2 spectrum
        sp2.set_title( 'Spectrum 2' )
        sp2.magnitude_spectrum( ch2, fs, scale = 'dB', color = 'C0', window = window )
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
# And display everything
plt.show()
