all: fw_DSO6021 fw_DSO6022BE fw_DSO6022BL fw_DDS120 fx2upload

DSO6021=PyHT6022/Firmware/DSO6021
DSO6022BE=PyHT6022/Firmware/DSO6022BE
DSO6022BL=PyHT6022/Firmware/DSO6022BL
DDS120=PyHT6022/Firmware/DDS120


.PHONY: fw_DSO6021
fw_DSO6021:
	cd $(DSO6021) && make


.PHONY: fw_DSO6022BE
fw_DSO6022BE:
	cd $(DSO6022BE) && make


.PHONY: fw_DSO6022BL
fw_DSO6022BL:
	cd $(DSO6022BL) && make


.PHONY: fw_DDS120
fw_DDS120:
	cd $(DDS120) && make


.PHONY: fx2upload
fx2upload:
	cd fx2upload && make


.PHONY: install
install: all
	-rm -rf build/*
	-rm -rf dist/*
	python3 setup.py install
	if [ -d /etc/udev/rules.d/ ]; then cp 60-hantek6022api.rules /etc/udev/rules.d/; fi
	install examples/*_6022*.py /usr/local/bin
	install fx2upload/fx2upload /usr/local/bin


.PHONY: deb
deb:
	fakeroot checkinstall --default --requires python3-libusb1 --install=no --backup=no --deldoc=yes


.PHONY: debinstall
debinstall: deb
	sudo dpkg -i `ls hantek6022api_*.deb | tail -1`


.PHONY: clean
clean:
	-rm *~ .*~
	-rm -rf build/*
	-rm -rf dist/*
	( cd $(DSO6021) && make clean )
	( cd $(DSO6022BE) && make clean )
	( cd $(DSO6022BL) && make clean )
	( cd $(DDS120) && make clean )
	( cd fx2upload && make clean )


.PHONY: xfer
xfer:
	cp $(DSO6021)/dso6021-firmware.hex \
	../OpenHantek6022/openhantek/res/firmware
	cp $(DSO6022BE)/dso6022be-firmware.hex \
	../OpenHantek6022/openhantek/res/firmware
	cp $(DSO6022BL)/dso6022bl-firmware.hex \
	../OpenHantek6022/openhantek/res/firmware
