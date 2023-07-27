all: fw_DSO6021 fw_DSO6022BE fw_DSO6022BL fw_DDS120 fx2upload fw_version

FIRMWARE=PyHT6022/Firmware
DSO6021=$(FIRMWARE)/DSO6021
DSO6022BE=$(FIRMWARE)/DSO6022BE
DSO6022BL=$(FIRMWARE)/DSO6022BL
DDS120=$(FIRMWARE)/DDS120
PYTHON=$(shell which python || which python3)

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


# firmware version synchronisation to OpenHantek
.PHONY:	fw_version
fw_version:
	@echo
	@./MK_FW_VERSION.sh | tee $(FIRMWARE)/dso602x_fw_version.h


# create a debian binary package
.PHONY:	deb
deb:	clean all changelog
	DEB_BUILD_OPTIONS=nocheck $(PYTHON) setup.py --command-packages=stdeb.command bdist_deb
	-rm -f hantek6022api_*_all.deb hantek6022api-*.tar.gz
	ln `ls deb_dist/hantek6022api_*_all.deb | tail -1` .
	ls -l deb_dist/hantek6022api_*_all.deb


# create a debian source package
.PHONY:	dsc
dsc:	clean all changelog
	DEB_BUILD_OPTIONS=nocheck $(PYTHON) setup.py --command-packages=stdeb.command sdist_dsc


.PHONY: debinstall
debinstall: deb
	sudo dpkg -i hantek6022api_*_all.deb


# remove all compiler and package build artefacts
.PHONY: clean
clean:
	$(PYTHON) setup.py clean
	-rm -rf *~ .*~ deb_dist dist *.tar.gz *.egg* build tmp
	( cd $(DSO6021) && make clean )
	( cd $(DSO6022BE) && make clean )
	( cd $(DSO6022BL) && make clean )
	( cd $(DDS120) && make clean )
	( cd fx2upload && make clean )


# remove all package builds
.PHONY:	distclean
distclean: clean
	-rm -f *.deb


# transfer the needed hex files to OpenHantek
.PHONY: xfer
xfer: all
	cp $(DSO6021)/dso6021-firmware.hex \
	../OpenHantek6022/openhantek/res/firmware
	cp $(DSO6022BE)/dso6022be-firmware.hex \
	../OpenHantek6022/openhantek/res/firmware
	cp $(DSO6022BL)/dso6022bl-firmware.hex \
	../OpenHantek6022/openhantek/res/firmware
	cp $(FIRMWARE)/dso602x_fw_version.h \
	../OpenHantek6022/openhantek/res/firmware
