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


# update the changelog from git
.PHONY:	changelog
changelog:
	git log --pretty="%cs: %s [%h]" > CHANGELOG


# create a debian binary package
.PHONY:	deb
deb:	all changelog distclean
	DEB_BUILD_OPTIONS=nocheck python setup.py --command-packages=stdeb.command bdist_deb
	ln `ls deb_dist/hantek6022api_*.deb | tail -1` .


# create a debian source package
.PHONY:	dsc
dsc:	all changelog distclean
	DEB_BUILD_OPTIONS=nocheck python setup.py --command-packages=stdeb.command sdist_dsc


.PHONY: debinstall
debinstall: deb
	sudo dpkg -i hantek6022api_*.deb


# remove all compiler artefacts
.PHONY: clean
clean:
	-rm *~ .*~
	( cd $(DSO6021) && make clean )
	( cd $(DSO6022BE) && make clean )
	( cd $(DSO6022BL) && make clean )
	( cd $(DDS120) && make clean )
	( cd fx2upload && make clean )


# remove all package build artefacts
.PHONY:	distclean
distclean:
	python setup.py clean
	-rm -rf *~ .*~ deb_dist dist *.tar.gz *.egg* *.deb build tmp


# transfer the needed hex files to OpenHantek
.PHONY: xfer
xfer: all
	cp $(DSO6021)/dso6021-firmware.hex \
	../OpenHantek6022/openhantek/res/firmware
	cp $(DSO6022BE)/dso6022be-firmware.hex \
	../OpenHantek6022/openhantek/res/firmware
	cp $(DSO6022BL)/dso6022bl-firmware.hex \
	../OpenHantek6022/openhantek/res/firmware
