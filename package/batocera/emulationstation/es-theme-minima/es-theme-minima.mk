################################################################################
#
# EmulationStation theme "Carbon"
#
################################################################################
# Version.: Commits on Feb 13, 2024
ES_THEME_MINIMA_VERSION = b8eebd0a80fab84e61674239d2236051dc3c1ce3
ES_THEME_MINIMA_SITE = $(call github,soaremicheledavid,es-theme-minima,$(ES_THEME_MINIMA_VERSION))

define ES_THEME_MINIMA_INSTALL_TARGET_CMDS
    mkdir -p $(TARGET_DIR)/usr/share/emulationstation/themes/es-theme-minima
    cp -r $(@D)/* $(TARGET_DIR)/usr/share/emulationstation/themes/es-theme-minima
endef

$(eval $(generic-package))
