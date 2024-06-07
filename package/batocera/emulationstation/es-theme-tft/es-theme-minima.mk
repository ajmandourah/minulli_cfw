################################################################################
#
# EmulationStation theme "tft"
#
################################################################################
# Version.: Commits on Feb 13, 2024
ES_THEME_TFT_VERSION = dc69025ad757cbe3827354f8a5fc4cfc26ff9481
ES_THEME_TFT_SITE = $(call github,ajmandourah,es-theme-tft,$(ES_THEME_TFT_VERSION))

define ES_THEME_TFT_INSTALL_TARGET_CMDS
    mkdir -p $(TARGET_DIR)/usr/share/emulationstation/themes/es-theme-tft
    cp -r $(@D)/* $(TARGET_DIR)/usr/share/emulationstation/themes/es-theme-tft
endef

$(eval $(generic-package))
