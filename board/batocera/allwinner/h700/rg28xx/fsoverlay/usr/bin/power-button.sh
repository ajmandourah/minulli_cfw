#!/bin/bash
# Suspend or shutdown

# Paths
POWER_BUTTON_STATE="/var/run/power-button-state.flag"
LOCK_FILE="/var/run/power-button-script.lock"

# Threshold for long press to shutdown (some boards cut power when power button is held too long)
LONG_PRESS_THRESHOLD=3

suspend_system() {
    if pidof retroarch >/dev/null; then
        /usr/bin/poweroff.sh
    fi
    pm-is-supported --suspend && pm-suspend
}

shutdown_system() {
    /usr/bin/poweroff.sh
}

exec 200>"${LOCK_FILE}"
flock -n 200 || exit 1

# Handle button press
echo "1" > "$POWER_BUTTON_STATE"

START_TIME=$(date +%s)
while true; do
    sleep 0.1  # Check the power button state every 0.1 seconds

    if [ "$(cat ${POWER_BUTTON_STATE})" = "0" ]; then
        # Power button released
        suspend_system
        break
    fi

    CURRENT_TIME=$(date +%s)
    DURATION=$((CURRENT_TIME - START_TIME))

    if [ "${DURATION}" -ge "${LONG_PRESS_THRESHOLD}" ]; then
        shutdown_system
        break
    fi
done

flock -u 200
rm -f "${LOCK_FILE}"

exit 0
