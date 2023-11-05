# Version is X.Y.Z = major.minor.update
#
# Keep major.minor in sync, ignore patch (used for deb version only):
# - PyHT6022/Firmware/DSO6022BE/descriptor.inc
#   Format: XX.YY.ZZ -> "FIRMWARE_VERSION = 0xYYXX"
# - PyHT6022/LibUsbScope.py
#   Format: XX.YY.ZZ -> "FIRMWARE_VERSION = 0xXXYY"
#
# Update also "const uint16_t DSO602x_FW_VER = 0xXXYY" in "OpenHantek6022/openhantek/res/firmware/dso602x_fw_version.h"

__version__ = '2.10.6'


from setuptools import setup
import os
import platform


# generic data files
data_files=[
    ( os.path.join( 'share', 'doc', 'hantek6022api' ), [ 'README.md', 'CHANGELOG', 'LICENSE' ] ),
]

# add linux specific config files and binaries
if platform.system() == 'Linux':
    data_files.append( ( '/etc/udev/rules.d/', [ 'udev/60-hantek6022api.rules' ] ) )
    data_files.append( ( 'bin/', [ 'fx2upload/fx2upload' ] ) )


setup(
    name='hantek6022api',
    author='Ho-Ro',
    author_email='horo@localhost',
    description='Python API and better FW for Hantek 6022 USB Oscilloscopes',
    long_description=
'''A Python API, tools for calibration, data capturing and visualisation
as well as an improved FW for Hantek 6022 USB Oscilloscopes''',
    platforms=[ 'all' ],
    version=__version__,
    license='GPLv2',
    # the required python packages
    install_requires=['libusb1', 'matplotlib', 'numpy'],
    url='https://github.com/Ho-Ro/Hantek6022API',
    packages=[ 'PyHT6022', 'PyHT6022.Firmware' ],
    package_data={
        'PyHT6022': [
            os.path.join( 'Firmware', 'DSO6022BE', 'dso6022be-firmware.hex' ),
            os.path.join( 'Firmware', 'DSO6022BL', 'dso6022bl-firmware.hex' ),
            os.path.join( 'Firmware', 'DSO6021', 'dso6021-firmware.hex' ),
            os.path.join( 'Firmware', 'DDS120', 'dds120-firmware.hex' ),
            os.path.join( 'Firmware', 'modded', 'mod_fw_01.ihex' ),
            os.path.join( 'Firmware', 'modded', 'mod_fw_iso.ihex' ),
            os.path.join( 'Firmware', 'stock', 'stock_fw.ihex' ),
        ]
    },
    include_package_data=True,
    # the python scripts that can be found via the PATH
    scripts=[
        os.path.join( 'examples', 'calibrate_6022.py' ),
        os.path.join( 'examples', 'capture_6022.py' ),
        os.path.join( 'examples', 'plot_from_capture_6022.py' ),
        os.path.join( 'examples', 'fft_from_capture_6022.py' ),
        os.path.join( 'examples', 'fft_ft_from_capture_6022.py' ),
        os.path.join( 'examples', 'set_cal_out_freq_6022.py' ),
        os.path.join( 'examples', 'upload_6022_firmware_from_hex.py' ),
        os.path.join( 'examples', 'upload_6022_firmware.py' ),
    ],
    # generic and linux 'data_files' from top
    data_files = data_files
)
