################################################################################
#
# EmulationStation theme "Carbon"
#
################################################################################
# Version.: Commits on Feb 13, 2024
ES_THEME_MINIMA_VERSION =
ES_THEME_MINIMA_SITE = https://github.com/soaremicheledavid/ES-Theme-MINIMA/archive/refs/heads/master.tar.gz

define ES_THEME_MINIMA_INSTALL_TARGET_CMDS
    mkdir -p $(TARGET_DIR)/usr/share/emulationstation/themes/es-theme-minima
    cp -r $(@D)/* $(TARGET_DIR)/usr/share/emulationstation/themes/es-theme-minima
endef

$(eval $(generic-package))
