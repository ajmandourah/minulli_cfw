#!/bin/sh

#alsactl store 0 -f /userdata/system/.asound.state

echo $(batocera-audio getSystemVolume) > /userdata/system/.volume
sync

reboot

