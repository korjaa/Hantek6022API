#!/usr/bin/python3

__author__ = 'Jochen Hoenicke'

from PyHT6022.LibUsbScope import Oscilloscope

scope = Oscilloscope()
scope.setup()
if not scope.open_handle():
    sys.exit( -1 )

firmware = scope.read_firmware(length=16*1024, chunk_len=32)
scope.close_handle()

print(firmware)
