#!/bin/sh

# Save ALSA mixer state
# alsactl store 0 -f /userdata/system/.asound.state

# Try to stop all processes cleanly
#/etc/init.d/rcK
sync
#vibrate feedback
echo 1 > /sys/class/power_supply/axp2202-battery/moto && sleep 0.1 && echo 0 > /sys/class/power_supply/axp2202-battery/moto

if pidof retroarch >/dev/null; then
    /usr/bin/quit_game.sh
fi

# Start a background process that waits for a timeout duration before forcing shutdown
( sleep 5 && reboot -f -p ) &

# Try a clean shutdown
shutdown -Ph now

# If we reach this point, the shutdown was successful and we can kill the background job
kill $!


