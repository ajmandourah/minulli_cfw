################################################################################
#
# EmulationStation theme "Minulli"
#
################################################################################
# Version.: Commits on Feb 13, 2024
ES_THEME_MINULLI_VERSION = dc9635f77728f324e51df4c2c92f8eba821fa29d
ES_THEME_MINULLI_SITE = $(call github,ajmandourah,es-theme-minulli,$(ES_THEME_MINULLI_VERSION))

define ES_THEME_MINULLI_INSTALL_TARGET_CMDS
    mkdir -p $(TARGET_DIR)/usr/share/emulationstation/themes/es-theme-minulli
    cp -r $(@D)/* $(TARGET_DIR)/usr/share/emulationstation/themes/es-theme-minulli
endef

$(eval $(generic-package))
