#!/bin/sh

#alsactl store 0 -f /userdata/system/.asound.state

#/etc/init.d/rcK
sync

echo 1 > /sys/class/power_supply/axp2202-battery/moto && sleep 0.1 && echo 0 > /sys/class/power_supply/axp2202-battery/moto
reboot

