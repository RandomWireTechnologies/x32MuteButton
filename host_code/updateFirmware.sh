#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
# First lets find the device
PRODUCT_PATH=`grep -rl "NeoKey Trinkey" /sys/bus/usb/devices/*/product`
if [ $? == 1 ]; then
	echo "No device found";
	exit 1;
fi
#echo "Product path = $PRODUCT_PATH"
DEVICE_PATH="$(dirname "${PRODUCT_PATH}")"
cd $DEVICE_PATH


# Next lets find the python drive
DRIVE=/dev/`find . | grep -Eo 'sd.1$'`

# Check for mount point
if [[ ! -d /mnt/key ]]; then
	sudo mkdir /mnt/key
fi
sudo mount $DRIVE /mnt/key
cd $SCRIPT_DIR
cd ../firmware
sudo cp code.py /mnt/key/
sudo umount /mnt/key/
