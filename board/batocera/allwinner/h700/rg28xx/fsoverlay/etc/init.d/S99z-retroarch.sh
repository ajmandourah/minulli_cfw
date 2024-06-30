#!/bin/bash

#Check if retroarch is running meaning that a game got resumed
if pidof retroarch >/dev/null; then
    while pidof retroarch >/dev/null; do sleep 0.1; done
    emulationstation-standalone &
fi

