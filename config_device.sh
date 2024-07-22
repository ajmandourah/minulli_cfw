#!/bin/bash

# Check if an argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: \$0 <rg28xx|rg35xx-plus|rg35xx-h>"
    exit 1
fi

# Argument (converted to lowercase for case-insensitivity)
ARG=$(echo $1 | tr '[:upper:]' '[:lower:]')

# Validate the argument and determine the replacement value
case $ARG in
    "rg28xx")
        REPLACEMENT="rg28xx"
        ;;
    "rg35xx-plus"|"rg35xx-h")
        REPLACEMENT="rg35xx-plus"
        ;;
    *)
        echo "Invalid argument. Only 'rg28xx', 'rg35xx-plus', or 'rg35xx-H' are allowed."
        exit 1
        ;;
esac

# Define file paths relative to the script location
SCRIPT_DIR=$(dirname $0)
CONFIG_FILE="$SCRIPT_DIR/configs/batocera-h700.board"
CONFIG_IN_FILE="$SCRIPT_DIR/package/batocera/core/batocera-system/Config.in"

# Function to update a line in a file if it doesn't match the replacement value
update_line_if_needed() {
    local file=$1
    local search_pattern=$2
    local replacement=$3

    if grep -q "$search_pattern" "$file"; then
        current_value=$(grep "$search_pattern" "$file" | sed -E "s/.*\/([^\/]*)\/patches.*/\1/")
        if [ "$current_value" != "$REPLACEMENT" ]; then
            sed -i "s|$search_pattern.*|$replacement|" "$file"
        fi
    else
        echo "Pattern not found in $file"
        exit 1
    fi
}

# Update configs/batocera-h700.board
if [ -f "$CONFIG_FILE" ]; then
    update_line_if_needed "$CONFIG_FILE" 'BR2_GLOBAL_PATCH_DIR=' "BR2_GLOBAL_PATCH_DIR=\"\$(BR2_EXTERNAL_BATOCERA_PATH)/board/batocera/patches \$(BR2_EXTERNAL_BATOCERA_PATH)/board/batocera/allwinner/patches \$(BR2_EXTERNAL_BATOCERA_PATH)/board/batocera/allwinner/h700/patches \$(BR2_EXTERNAL_BATOCERA_PATH)/board/batocera/allwinner/h700/$REPLACEMENT/patches \""
    update_line_if_needed "$CONFIG_FILE" 'BR2_ROOTFS_OVERLAY=' "BR2_ROOTFS_OVERLAY=\"\$(BR2_EXTERNAL_BATOCERA_PATH)/board/batocera/fsoverlay \$(BR2_EXTERNAL_BATOCERA_PATH)/board/batocera/allwinner/h700/fsoverlay \$(BR2_EXTERNAL_BATOCERA_PATH)/board/batocera/allwinner/h700/$REPLACEMENT/fsoverlay \""
else
    echo "File $CONFIG_FILE not found!"
    exit 1
fi

# Update package/batocera/core/batocera-system/Config.in
if [ -f "$CONFIG_IN_FILE" ]; then
    update_line_if_needed "$CONFIG_IN_FILE" 'default "allwinner/h700/' "default \"allwinner/h700/$REPLACEMENT\" if BR2_PACKAGE_BATOCERA_TARGET_H700"
else
    echo "File $CONFIG_IN_FILE not found!"
    exit 1
fi

echo "Files updated successfully."
