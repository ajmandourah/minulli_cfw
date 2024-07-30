#!/bin/sh

#check if RA is running.
display="/sys/kernel/debug/dispdbg"

echo disp0 > $display/name
echo blank > $display/command
echo 1 > $display/param
echo 1 > $display/start

while pidof retroarch >/dev/null; do /usr/bin/retroarch --verbose --command QUIT; sleep 0.1; done
touch /userdata/system/.last

