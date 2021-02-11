#!/bin/sh

./read_eeprom_256_byte.py
od -Ax -tx1 -v eeprom_256.dat | tee eeprom_256.dump
