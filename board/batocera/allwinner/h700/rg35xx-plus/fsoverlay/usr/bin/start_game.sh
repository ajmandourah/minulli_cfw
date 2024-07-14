#!/bin/bash

RAHISTORY=/userdata/system/configs/retroarch/content_history.lpl
RACONFIG=/userdata/system/configs/retroarch/retroarchcustom.cfg
RACORECONFIG=/userdata/system/configs/retroarch/cores/retroarch-core-options.cfg
RAEXTRA=/tmp/tmp.cfg

Last_Game=`grep '"path":' ${RAHISTORY} | head -1`
Last_Core=`grep '"core_path":' ${RAHISTORY} | head -1`
Last_Game="${Last_Game%\"*}"
Last_Game="${Last_Game##*\"}"
Last_Core="${Last_Core%\"*}"
Last_Core="${Last_Core##*/}"

if [ -f /userdata/system/.last ]; then
    rm -f /userdata/system/.last
    touch $RAEXTRA
    echo 'savestate_auto_load = "true"' > $RAEXTRA
    echo "core_options_path = ${RACORECONFIG}" >> $RAEXTRA
    /usr/bin/retroarch -c "$RACONFIG" --appendconfig=/tmp/tmp.cfg -L "$Last_Core" "$Last_Game"
    rm -f $RAEXTRA
fi
