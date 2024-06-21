################################################################################
#
# EmulationStation theme "Minulli"
#
################################################################################
# Version.: Commits on Feb 13, 2024
ES_THEME_MINULLI_VERSION = c0b10a4452c360d6b84e59406652226c22e863e6
ES_THEME_MINULLI_SITE = $(call github,ajmandourah,es-theme-minulli,$(ES_THEME_MINULLI_VERSION))

define ES_THEME_MINULLI_INSTALL_TARGET_CMDS
    mkdir -p $(TARGET_DIR)/usr/share/emulationstation/themes/es-theme-minulli
    cp -r $(@D)/* $(TARGET_DIR)/usr/share/emulationstation/themes/es-theme-minulli
endef

$(eval $(generic-package))
