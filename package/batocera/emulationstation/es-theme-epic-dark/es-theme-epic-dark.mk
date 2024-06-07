################################################################################
#
# EmulationStation theme "Epic Dark"
#
################################################################################
# Version.: Commits on May 17, 2024
ES_THEME_EPIC_DARK_VERSION = d4ad8f1fcce8312eb2389ebbf8efb181dd2c9eae
ES_THEME_EPIC_DARK_SITE = $(call github,torresflo,es-theme-epic-dark,$(ES_THEME_EPIC_DARK_VERSION))

define ES_THEME_EPIC_DARK_INSTALL_TARGET_CMDS
    mkdir -p $(TARGET_DIR)/usr/share/emulationstation/themes/es-theme-epic-dark
    cp -r $(@D)/* $(TARGET_DIR)/usr/share/emulationstation/themes/es-theme-epic-dark
endef

$(eval $(generic-package))

