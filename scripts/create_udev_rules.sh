#!/bin/bash

echo "remap the device serial port(ttyUSBX) to coulomb_counter_cc75"
echo "coulomb_counter_cc75 usb connection as /dev/coulomb_counter_cc75, check it using the command : ls -l /dev|grep ttyUSB"
echo "start copy coulomb_counter_cc75.rules to  /lib/udev/rules.d/"
echo "`rospack find coulomb_counter_cc75_ros`/scripts/coulomb_counter_cc75.rules"
sudo cp `rospack find coulomb_counter_cc75_ros`/scripts/coulomb_counter_cc75.rules  /lib/udev/rules.d
echo " "
echo "Restarting udev"
echo ""
sudo service udev reload
sudo service udev restart
echo "finish "
