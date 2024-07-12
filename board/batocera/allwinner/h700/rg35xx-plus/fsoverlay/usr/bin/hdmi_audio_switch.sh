#!/bin/sh

# Path to the HDMI state file
hdmi_state_file="/sys/devices/platform/soc/6000000.hdmi/extcon/hdmi/state"

check_ingame() {
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:1234/runningGame")
    if [ $? -ne 0 ]; then
        return 0
    fi
    if [ "$HTTP_STATUS" -eq 201 ]; then
        return 1
    else
        return 0
    fi
}

if check_ingame; then
    exit 1
fi

# Check if debugfs is mounted
if grep -qs 'debugfs' /proc/mounts; then
    echo "debugfs is mounted." >> /var/log/hdmi-event.log
else
    echo "debugfs is not mounted. Attempting to mount..." >> /var/log/hdmi-event.log
    mount -t debugfs debugfs /sys/kernel/debug
    if [ $? -eq 0 ]; then
        echo "debugfs successfully mounted." >> /var/log/hdmi-event.log
    else
        echo "Failed to mount debugfs." >> /var/log/hdmi-event.log
        exit 1
    fi
fi

kill_es() {
	killall emulationstation 2>/dev/null
	killall touchegg 2>/dev/null
	if [ $? -eq 0 ]; then
		sleep 20 &
		watchdog=$!
		while ! [ -z $(pidof emulationstation) ]; do
			sleep 0.25
			$(kill -0 $watchdog) || exit
		done
		kill -9 $watchdog
	fi
}

state=$(cat "$hdmi_state_file")

echo "$(date) - HDMI event triggered - ${state}" >> /var/log/hdmi-event.log

if [ "$state" = "HDMI=1" ]; then
    sleep 1
    batocera-audio set alsa_output._sys_devices_platform_soc_soc_03000000_ahub1_mach_sound_card2.stereo-fallback
    batocera-resolution setOutput
    echo "HDMI CONNECTED!" >> /var/log/hdmi-event.log
    kill_es

else
    if check_ingame; then
	    exit 1
	fi
	
	sleep 1
	batocera-audio set alsa_output._sys_devices_platform_soc_soc_03000000_codec_mach_sound_card0.stereo-fallback
    batocera-resolution setOutput
    echo "HDMI DISCONNECTED!" >> /var/log/hdmi-event.log
    kill_es
fi

exit 0
