#!/usr/bin/python3

__author__ = 'Robert Cope'

from Hantek6022B import Hantek6022B
import pylab
import time
import sys
import argparse

samplerates = ( 20, 32, 50, 64, 100, 128, 200, 500, 1000, 2000, 4000, 8000, 10000 )
samplerate_help = "sample rate in kS/s ("
for samplerate in samplerates:
    samplerate_help +=  str( samplerate ) + ", "
samplerate_help += f"default: {samplerates[0]})"

gains = ( 1, 2, 5, 10 )
gain_help = "channel gain ("
for gain in gains:
    gain_help +=  str( gain ) + ", "
gain_help += f"default: {gains[0]})"

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser(
    prog='scopevis.py',
    description='Capture data from Hantek6022' )
ap.add_argument( "--ac1", action = "store_true", default = False, help = "AC coupling for CH1" )
ap.add_argument( "--ac2", action = "store_true", default = False, help = "AC coupling for CH2" )
ap.add_argument( "-b", "--blocks", type = int, default = 20, help="number of 1K sample blocks, default: 20" )
ap.add_argument( "--ch1", type = int, default = gains[0], help=f"select gain for ch1 (1, 2, 5, 10, default: {gains[0]})" )
ap.add_argument( "--ch2", type = int, default = 0, help="sample also ch2 with gain 1, 2, 5, 10" )
ap.add_argument( "-f", "--frequency", type = int, default = 0, help="set cal out frequency in Hz" )
ap.add_argument( "-s", "--samplerate", type = int, default = samplerates[0], help=samplerate_help )

options = ap.parse_args()
argerr = False
if options.ch1 and options.ch1 not in gains:
    print( "error, ch1 gain must be one of:", gains )
    argerr = True
if options.ch2 and options.ch2 not in gains:
    print( "error, ch2 gain must be one of:", gains )
    argerr = True
if options.samplerate not in samplerates:
    print( "error, rate must be one of:", samplerates )
    argerr = True
if argerr:
    sys.exit()

data_points = options.blocks * 1024

# skip first 2K samples due to unstable xfer
skip = 2 * 1024
data_points += skip

scope = Hantek6022B()
scope.setup()
scope.open_handle()

# upload correct firmware into device's RAM
if (not scope.is_device_firmware_present):
    scope.flash_firmware()

# calculate and set the sample rate ID from real sample rate value
if options.samplerate < 1e3:
    sample_id = int( round( 100 + options.samplerate / 10 ) ) # 20k..500k -> 102..150
else:
    sample_id = int( round( options.samplerate / 1e3 ) ) # 1000k -> 1

scope.set_sample_rate( sample_id )

if options.ch1:
    scope.set_ch1_voltage_range( options.ch1 )
if options.ac1:
    scope.set_ch1_ac_dc( scope.AC )
else:
    scope.set_ch1_ac_dc( scope.DC )

if options.ch2:
    scope.set_num_channels( 2 )
    scope.set_ch2_voltage_range( options.ch2 )
    if options.ac2:
        scope.set_ch2_ac_dc( scope.AC )
    else:
        scope.set_ch2_ac_dc( scope.DC )
else:
    scope.set_ch2_voltage_range( 1 )

# read and apply calibration values from EEPROM
calibration = scope.get_calibration_values()

if options.frequency:
    scope.set_calibration_frequency( options.frequency )

time.sleep( 0.1 )


ch1_data, ch2_data = scope.read_data(data_points)#,raw=True)#timeout=1)

if options.ch1:
    voltage_data1 = scope.scale_read_data(ch1_data[skip:], options.ch1, channel=1 )
if options.ch2:
    voltage_data2 = scope.scale_read_data(ch2_data[skip:], options.ch2, channel=2 )
timing_data, rate_label = scope.convert_sampling_rate_to_measurement_times(data_points-skip, sample_id)
scope.close_handle()


pylab.title( f'{options.blocks}K samples @ {rate_label}')
if options.ch1:
    pylab.plot(timing_data, voltage_data1, color='#C00000', label='CH1')
if options.ch2:
    pylab.plot(timing_data, voltage_data2, color='#0000C0', label='CH2')

pylab.xlabel('Time (s)')
pylab.ylabel('Voltage (V)')
pylab.grid()
pylab.legend(loc='best')
pylab.xticks(rotation=30)
pylab.tight_layout()
pylab.show()
