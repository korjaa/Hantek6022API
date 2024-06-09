#!/usr/bin/python3

__author__ = 'Robert Cope'

import sys
from Hantek6022B.Firmware import stock_firmware as Firmware
from Hantek6022B import Hantek6022B

scope = Hantek6022B()
scope.setup()
if not scope.open_handle():
    sys.exit( -1 )
scope.flash_firmware( firmware = Firmware )
scope.close_handle()
