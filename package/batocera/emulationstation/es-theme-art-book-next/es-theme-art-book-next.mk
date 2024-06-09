################################################################################
#
# EmulationStation theme "Art Book Next"
#
################################################################################
# Version.: Commits on June 5, 2024
ES_THEME_ART_BOOK_NEXT_VERSION = df555df23b04fd5fc5acb2ebb680fdb617b4158b
ES_THEME_ART_BOOK_NEXT_SITE = $(call github,anthonycaccese,art-book-next-es,$(ES_THEME_ART_BOOK_NEXT_VERSION))

define ES_THEME_ART_BOOK_NEXT_INSTALL_TARGET_CMDS
    mkdir -p $(TARGET_DIR)/usr/share/emulationstation/themes/es-theme-art-book-next
    cp -r $(@D)/* $(TARGET_DIR)/usr/share/emulationstation/themes/es-theme-art-book-next
endef

$(eval $(generic-package))
