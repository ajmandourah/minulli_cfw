#!/bin/sh

#check if RA is running.
while pidof retroarch >/dev/null; do /usr/bin/retroarch --verbose --command QUIT; dd if=/dev/zero of=/dev/fb0; sleep 0.1; done
touch /userdata/system/.last

