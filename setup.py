__version__ = '2.10.2'


from setuptools import setup
import os

setup(
    name='hantek6022api',
    author='Ho-Ro',
    author_email='horo@localhost',
    description='Python API and better FW for Hantek 6022 USB Oscilloscopes',
    long_description=
'''A Python API, tools for calibration, data capturing and visualisation
as well as an improved FW for Hantek 6022 USB Oscilloscopes''',
    platforms=['all'],
    version=__version__,
    license='GPLv2',
    url='https://github.com/Ho-Ro/Hantek6022API',
    packages=['PyHT6022', 'PyHT6022.Firmware'],
    package_data={'PyHT6022': [os.path.join('Firmware', 'DSO6022BE', 'dso6022be-firmware.hex'),
                               os.path.join('Firmware', 'DSO6022BL', 'dso6022bl-firmware.hex'),
                               os.path.join('Firmware', 'DSO6021', 'dso6021-firmware.hex'),
                               os.path.join('Firmware', 'DDS120', 'dds120-firmware.hex'),
                               os.path.join('Firmware', 'modded', 'mod_fw_01.ihex'),
                               os.path.join('Firmware', 'modded', 'mod_fw_iso.ihex'),
                               os.path.join('Firmware', 'stock', 'stock_fw.ihex'),]
    },
    include_package_data=True,
    install_requires=['libusb1', 'matplotlib'],
    data_files=[
        ("/usr/bin/", ["examples/calibrate_6022.py",
                       "examples/capture_6022.py",
                       "examples/plot_from_capture_6022.py",
                       "examples/fft_from_capture_6022.py",
                       "examples/fft_ft_from_capture_6022.py",
                       "examples/set_cal_out_freq_6022.py",
                       "examples/upload_6022_firmware_from_hex.py",
                       "examples/upload_6022_firmware.py",
                       "fx2upload/fx2upload"]
        ),
        ("/usr/share/doc/hantek6022api/", ["README.md"]),
        ("/usr/share/doc/hantek6022api/", ["CHANGELOG"]),
        ("/usr/share/doc/hantek6022api/", ["LICENSE"]),
        ("/etc/udev/rules.d/", ["udev/60-hantek6022api.rules"]),
    ]
)
