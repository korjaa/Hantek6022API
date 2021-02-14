__author__ = 'Robert Cope'
__version__ = '0.0.2'

from setuptools import setup
import os

setup(name='Python Hantek 6022BE Wrapper',
      author=__author__,
      author_email='rpcope1@gmail.com',
      description='A Python API for using the inexpensive Hantek 6022BE USB Oscilloscope in Linux',
      version=__version__,
      license='GPLv2',
      packages=['PyHT6022', 'PyHT6022.Firmware'],
      package_data={'PyHT6022': [os.path.join('Firmware', 'DSO6022BE', 'dso6022be-firmware.hex'),
                                 os.path.join('Firmware', 'DSO6022BL', 'dso6022bl-firmware.hex'),
                                 os.path.join('Firmware', 'DSO6021', 'dso6021-firmware.hex'),
                                 os.path.join('Firmware', 'DDS120', 'dds120-firmware.hex'),
                                 os.path.join('Firmware', 'modded', 'mod_fw_01.ihex'),
                                 os.path.join('Firmware', 'modded', 'mod_fw_iso.ihex'),
                                 os.path.join('Firmware', 'stock', 'stock_fw.ihex'),]},
      include_package_data=True,
      install_requires=['libusb1'])
