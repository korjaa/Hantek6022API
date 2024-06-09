#!/usr/bin/python3

__author__ = 'Jochen Hoenicke'

import sys
from Hantek6022B import Hantek6022B

scope = Hantek6022B()
scope.setup()
if not scope.open_handle():
    sys.exit( -1 )

firmware = scope.read_firmware(length=16*1024, chunk_len=32)
scope.close_handle()

print(firmware)
