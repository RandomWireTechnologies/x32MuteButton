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
DRIVE=/dev/`find . | grep -Eo 'sd.$'`

# Check for mount point
if [[ ! -d /mnt/key ]]; then
	sudo mkdir /mnt/key
fi
sudo mount $DRIVE /mnt/key

# Check to see if we're in the bootloader
if [[ ! -f "/mnt/key/INFO_UF2.TXT" ]]; then
	echo "Not in bootloader, you must double click the reset button first!"
	sudo umount /mnt/key
	exit 1;
fi
cd $SCRIPT_DIR
cd ../firmware
FIRMWARE=$(ls *.uf2 | head -1)
echo "Installing $FIRMWARE onto device..."
sudo cp $FIRMWARE /mnt/key/
sudo umount /mnt/key/
echo "Firmware copied...waitin 3 seconds to ensure update"
sleep 3
echo "Installing python code"
cd $SCRIPT_DIR
./updateFirmware.sh
