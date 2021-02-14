#!/usr/bin/python3

"""
Flash default firmware into device
ither firmare-DSO6022BE or firmware-DSO6022BL or firmware-DSO6021
depending on VID/PID
"""

from PyHT6022.LibUsbScope import Oscilloscope

scope = Oscilloscope()
scope.setup()
scope.open_handle()
scope.flash_firmware()
print( "FW version", hex( scope.get_fw_version() ) )
scope.close_handle()
