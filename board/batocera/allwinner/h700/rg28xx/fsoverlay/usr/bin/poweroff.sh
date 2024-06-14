#!/bin/sh

# LAST_GAME=`grep '"path":' ${RA_CONTENT_HISTORY} | head -1`
# LAST_CORE=
#
# function retroarch_down()
# {
#     while pidof retroarch > /dev/null; do /usr/bin/retroarch --verbose --command QUIT; sleep 0.1; done
#     touch /userdata/.last
#     sync
#     shutdown -h now
#     while true; do sleep 5; done
#
# }
# Save ALSA mixer state
# alsactl store 0 -f /userdata/system/.asound.state

# Try to stop all processes cleanly
# /etc/init.d/rcK
echo $(batocera-audio getSystemVolume) > /userdata/system/.volume
sync

# Start a background process that waits for a timeout duration before forcing shutdown
( sleep 5 && reboot -f -p ) &

# Try a clean shutdown
shutdown -Ph now

# If we reach this point, the shutdown was successful and we can kill the background job
kill $!


