#!/bin/sh

# extract version (MAJOR and minor) from FW source
# version is stored as byte swapped word (0xmmMM)
# format as uint16_t 0xMMmm
# write header file for OpenHantek6022


MINORMAJOR=`grep -Eo "FIRMWARE_VERSION[[:space:]]+=[[:space:]]+0x[0-9]{4}" PyHT6022/Firmware/DSO6022BE/descriptor.inc | cut -dx -f2`

MINOR=`echo $MINORMAJOR | cut -b1-2`
MAJOR=`echo $MINORMAJOR | cut -b3-4`

echo "// SPDX-License-Identifier: GPL-3.0-or-later"
echo
echo "#pragma once"
echo
echo "#include <stdint.h>"
echo
echo "const uint16_t DSO602x_FW_VER = 0x${MAJOR}${MINOR};"
echo
echo "// setup.py: $(grep -Eo __version__[[:space:]]+=[[:space:]]+\'[0-9]{1,2}.[0-9]{1,2}.[0-9]{1,2}\' setup.py)"
echo "// PyHT6022/LibUsbScope.py: $(grep -Eo FIRMWARE_VERSION[[:space:]]+=[[:space:]]+0x[0-9]{4} PyHT6022/LibUsbScope.py)"
echo "// PyHT6022/Firmware/DSO6022BE/descriptor.inc: $(grep -Eo 'FIRMWARE_VERSION[[:space:]]+=[[:space:]]+0x[0-9]{4}' PyHT6022/Firmware/DSO6022BE/descriptor.inc)"
echo
