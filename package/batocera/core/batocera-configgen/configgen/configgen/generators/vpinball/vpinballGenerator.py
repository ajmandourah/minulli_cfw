#!/usr/bin/env python

import os
import configparser
import Command
from generators.Generator import Generator
import batoceraFiles
import shutil
from utils.logger import get_logger
import controllersConfig
from utils.batoceraServices import batoceraServices
import utils.videoMode as videoMode

eslog = get_logger(__name__)

vpinballConfigPath     = batoceraFiles.CONF + "/vpinball"
vpinballConfigFile     = vpinballConfigPath + "/VPinballX.ini"
vpinballPinmameIniPath = batoceraFiles.CONF + "/vpinball/pinmame/ini"

class VPinballGenerator(Generator):

    def generate(self, system, rom, playersControllers, metadata, guns, wheels, gameResolution):

        screens = videoMode.getScreensInfos(system.config)

        # create vpinball config directory and default config file if they don't exist
        if not os.path.exists(vpinballConfigPath):
            os.makedirs(vpinballConfigPath)
        if not os.path.exists(vpinballPinmameIniPath):
            os.makedirs(vpinballPinmameIniPath)
        if not os.path.exists(vpinballConfigFile):
            shutil.copy("/usr/bin/vpinball/assets/Default_VPinballX.ini", vpinballConfigFile)

        ## [ VPinballX.ini ] ##
        try:
            vpinballSettings = configparser.ConfigParser(interpolation=None, allow_no_value=True)
            vpinballSettings.optionxform = str
            vpinballSettings.read(vpinballConfigFile)
        except configparser.DuplicateOptionError as e:
            eslog.debug(f"Error reading VPinballX.ini: {e}")
            eslog.debug(f"*** Using default VPinballX.ini file ***")
            shutil.copy("/usr/bin/vpinball/assets/Default_VPinballX.ini", vpinballConfigFile)
            vpinballSettings = configparser.ConfigParser(interpolation=None, allow_no_value=True)
            vpinballSettings.optionxform = str
            vpinballSettings.read(vpinballConfigFile)
        # Sections
        if not vpinballSettings.has_section("Standalone"):
            vpinballSettings.add_section("Standalone")
        if not vpinballSettings.has_section("Player"):
            vpinballSettings.add_section("Player")

        #Tables are organised by folders containing the vpx file, and sub-folders with the roms, altcolor, altsound,...
        # We keep a switch to allow users with the old unique pinmame to be able to continue using vpinball (switchon)
        if system.isOptSet("vpinball_folders") and system.getOptBoolean("vpinball_folders") == False:
            vpinballSettings.set("Standalone", "PinMAMEPath", "")
        else:
            vpinballSettings.set("Standalone", "PinMAMEPath", "./")
        #Ball trail
        if system.isOptSet("vpinball_balltrail"):
            vpinballSettings.set("Player", "BallTrail", "1")
            vpinballSettings.set("Player", "BallTrailStrength", system.config["vpinball_balltrail"])
        else:
            vpinballSettings.set("Player", "BallTrail", "0")
            vpinballSettings.set("Player", "BallTrailStrength", "0")
        #Visual Nugde Strength
        if system.isOptSet("vpinball_nudgestrength"):
            vpinballSettings.set("Player", "NudgeStrength", system.config["vpinball_nudgestrength"])
        else:
            vpinballSettings.set("Player", "NudgeStrength", "")
        # Performance settings
        if system.isOptSet("vpinball_maxframerate"):
            vpinballSettings.set("Player", "MaxFramerate", system.config["vpinball_maxframerate"])
        else:
            vpinballSettings.set("Player", "MaxFramerate", "")
        if system.isOptSet("vpinball_vsync"):
            vpinballSettings.set("Player", "SyncMode", system.config["vpinball_vsync"])
        else:
            vpinballSettings.set("Player", "SyncMode", "2")
        if system.isOptSet("vpinball_presets"):
            if system.config["vpinball_presets"]=="defaults":
                vpinballSettings.set("Player", "FXAA", "")
                vpinballSettings.set("Player", "Sharpen", "")
                vpinballSettings.set("Player", "DisableAO", "")
                vpinballSettings.set("Player", "DynamicAO", "")
                vpinballSettings.set("Player", "SSRefl", "")
                vpinballSettings.set("Player", "PFReflection", "")
                vpinballSettings.set("Player", "ForceAnisotropicFiltering", "")
                vpinballSettings.set("Player", "AlphaRampAccuracy", "")
            if system.config["vpinball_presets"]=="highend":
                vpinballSettings.set("Player", "FXAA", "3")
                vpinballSettings.set("Player", "Sharpen", "2")
                vpinballSettings.set("Player", "DisableAO", "0")
                vpinballSettings.set("Player", "DynamicAO", "1")
                vpinballSettings.set("Player", "SSRefl", "1")
                vpinballSettings.set("Player", "PFReflection", "5")
                vpinballSettings.set("Player", "ForceAnisotropicFiltering", "1")
                vpinballSettings.set("Player", "AlphaRampAccuracy", "10")
            if system.config["vpinball_presets"]=="lowend":
                vpinballSettings.set("Player", "FXAA", "0")
                vpinballSettings.set("Player", "Sharpen", "0")
                vpinballSettings.set("Player", "DisableAO", "1")
                vpinballSettings.set("Player", "DynamicAO", "0")
                vpinballSettings.set("Player", "SSRefl", "0")
                vpinballSettings.set("Player", "PFReflection", "3")
                vpinballSettings.set("Player", "ForceAnisotropicFiltering", "0")
                vpinballSettings.set("Player", "AlphaRampAccuracy", "5")
            # if nothing is specified, we're in manual settings, ie we don't change any value in the config file
            # regarding performance settings

        # disable full screen to move the window if necessary
        vpinballSettings.set("Player", "FullScreen", "0")

        #Altcolor (switchon)
        if system.isOptSet("vpinball_altcolor") and system.getOptBoolean("vpinball_altcolor") == False:
            vpinballSettings.set("Standalone", "AltColor", "0")
        else:
            vpinballSettings.set("Standalone", "AltColor","1")

        # Extra_windows (pinmamedmd, flexdmd, b2s,b2sdmd)
        # VideogetCurrentResolution to convert from percentage to pixel value
        # necessary trick because people can plug their 1080p laptop on a 4k TV
        # (and because VPinballX.ini uses absolute pixel coordinates)
        def ConvertToPixel(total_size,percentage):
            pixel_value = str(int(int(total_size)*float(percentage)*1e-2))
            return pixel_value
        # Calculates the relative height, depending on the screen ratio
        # (normaly 16/9), the element ratio (4/3 for the b2s) and the relative width
        def RelativeHeightCalculate(Rscreen,Relement,RelativeWidth):
            return int(Rscreen*RelativeWidth/Relement)
        # Reasonable constants / default values
        Rscreen=16/9
        small,medium,large=20,25,30
        x,y,width=0,0,medium

        # which windows to display, and where ?

        # flexdmd
        vpinball_flexdmd_val = ""
        if system.isOptSet("vpinball_flexdmd"):
            vpinball_flexdmd_val = system.config["vpinball_flexdmd"]
        if vpinball_flexdmd_val == "":
            if len(screens) > 2:
                vpinball_flexdmd_val = "screen3"
            else:
                vpinball_flexdmd_val = "flexdmd_disabled"
        if len(screens) <= 1 and vpinball_flexdmd_val == "screen2":
            vpinball_flexdmd_val = "flexdmd_disabled"
        if len(screens) <= 2 and vpinball_flexdmd_val == "screen3":
            vpinball_flexdmd_val = "flexdmd_disabled"

        # pinmame : same as flexdmd (and both should never be displayed at the same time)
        vpinball_pinmame_val = ""
        if system.isOptSet("vpinball_pinmame"):
            vpinball_pinmame_val = system.config["vpinball_pinmame"]
        if vpinball_pinmame_val == "":
            if len(screens) > 2:
                vpinball_pinmame_val = "screen3"
            else:
                vpinball_pinmame_val = "pinmame_disabled"
        if len(screens) <= 1 and vpinball_pinmame_val == "screen2":
            vpinball_pinmame_val = "pinmame_disabled"
        if len(screens) <= 2 and vpinball_pinmame_val == "screen3":
            vpinball_pinmame_val = "pinmame_disabled"
        
        # b2s
        vpinball_b2s_val = ""
        if system.isOptSet("vpinball_b2s"):
            vpinball_b2s_val = system.config["vpinball_b2s"]

        if vpinball_b2s_val == "":
            if len(screens) > 1:
                vpinball_b2s_val = "screen2"
            else:
                vpinball_b2s_val = "b2s_disabled"

        if len(screens) <= 1 and vpinball_b2s_val == "screen2":
            vpinball_b2s_val = "b2s_disabled"

        #
        reverse_playfield_and_b2s = False
        if system.isOptSet("vpinball_inverseplayfieldandb2s") and system.getOptBoolean("vpinball_inverseplayfieldandb2s"):
            reverse_playfield_and_b2s = True

        playFieldScreen = 0
        backglassScreen = 1
        if reverse_playfield_and_b2s and len(screens) > 1:
            playFieldScreen = 1
            backglassScreen = 0

        # playfield
        vpinballSettings.set("Player", "WindowPosX", str(screens[playFieldScreen]["x"]))
        vpinballSettings.set("Player", "WindowPosY", str(screens[playFieldScreen]["y"]))
        vpinballSettings.set("Player", "Width",      str(screens[playFieldScreen]["width"]))
        vpinballSettings.set("Player", "Height",     str(screens[playFieldScreen]["height"]))

        # PinMame
        WindowName="PinMAMEWindow"
        Rwindow = 4/1   #Usual Ratio for this window
        # Auto default behaviour is to read values from VPinballX.ini file
        # so we don't do anything in the configgen
        if vpinball_pinmame_val=="pinmame_disabled":
            vpinballSettings.set("Standalone", WindowName,"0")
        elif vpinball_pinmame_val=="screen2":
            vpinballSettings.set("Standalone", WindowName,"1")
            if vpinball_b2s_val=="screen2": # share with b2s screen ?
                vpinballSettings.set("Standalone", WindowName,"1")
                vpinballSettings.set("Standalone", WindowName+"X",      str(screens[backglassScreen]["x"]+(screens[backglassScreen]["width"]-1024)//2))
                vpinballSettings.set("Standalone", WindowName+"Y",      str(screens[backglassScreen]["y"]))
                vpinballSettings.set("Standalone", WindowName+"Width",  str(1024))
                vpinballSettings.set("Standalone", WindowName+"Height", str(256))
            else:
                width  = screens[backglassScreen]["width"]
                height = (screens[backglassScreen]["width"] // 128 * 32)
                y = (screens[backglassScreen]["height"]-height)//2
                vpinballSettings.set("Standalone", WindowName,"1")
                vpinballSettings.set("Standalone", WindowName+"X",      str(screens[backglassScreen]["x"]))
                vpinballSettings.set("Standalone", WindowName+"Y",      str(screens[backglassScreen]["y"]+y))
                vpinballSettings.set("Standalone", WindowName+"Width",  str(width))
                vpinballSettings.set("Standalone", WindowName+"Height", str(height))
        elif vpinball_pinmame_val=="screen3":
            vpinballSettings.set("Standalone", WindowName,"1")
            vpinballSettings.set("Standalone", WindowName+"X",      str(screens[2]["x"]))
            vpinballSettings.set("Standalone", WindowName+"Y",      str(screens[2]["y"]))
            vpinballSettings.set("Standalone", WindowName+"Width",  str(screens[2]["width"]))
            vpinballSettings.set("Standalone", WindowName+"Height", str(screens[2]["height"]))
        else:
            vpinballSettings.set("Standalone", WindowName,"1")
            if vpinball_pinmame_val=="pinmame_topright_small":
                width=small
                x=100-width
            if vpinball_pinmame_val=="pinmame_topright_medium":
                width=medium
                x=100-width
            if vpinball_pinmame_val=="pinmame_topright_large":
                width=large
                x=100-width
            if vpinball_pinmame_val=="pinmame_topleft_small":
                width=small
                x=0
            if vpinball_pinmame_val=="pinmame_topleft_medium":
                width=medium
                x=0
            if vpinball_pinmame_val=="pinmame_topleft_large":
                width=large
                x=0
            # apply settings
            height=RelativeHeightCalculate(Rscreen,Rwindow,width)
            vpinballSettings.set("Standalone",WindowName+"X",ConvertToPixel(gameResolution["width"],x))
            vpinballSettings.set("Standalone",WindowName+"Y",ConvertToPixel(gameResolution["height"],y))
            vpinballSettings.set("Standalone",WindowName+"Width",ConvertToPixel(gameResolution["width"],width))
            vpinballSettings.set("Standalone",WindowName+"Height",ConvertToPixel(gameResolution["height"],height))

        # FlexDMD
        WindowName="FlexDMDWindow"
        Rwindow=4/1   #Usual Ratio for this window
        # Auto default behaviour is to read values from VPinballX.ini file
        # so we don't do anything in the configgen
        if vpinball_flexdmd_val=="flexdmd_disabled":
            vpinballSettings.set("Standalone", WindowName,"0")
        elif vpinball_flexdmd_val=="screen2":
            vpinballSettings.set("Standalone", WindowName,"1")
            if vpinball_b2s_val=="screen2": # share with b2s screen ?
                vpinballSettings.set("Standalone", WindowName,"1")
                vpinballSettings.set("Standalone", WindowName+"X",      str(screens[backglassScreen]["x"]+(screens[backglassScreen]["width"]-1024)//2))
                vpinballSettings.set("Standalone", WindowName+"Y",      str(screens[backglassScreen]["y"]))
                vpinballSettings.set("Standalone", WindowName+"Width",  str(1024))
                vpinballSettings.set("Standalone", WindowName+"Height", str(256))
            else:
                width  = screens[backglassScreen]["width"]
                height = (screens[backglassScreen]["width"] // 128 * 32)
                y = (screens[backglassScreen]["height"]-height)//2
                vpinballSettings.set("Standalone", WindowName,"1")
                vpinballSettings.set("Standalone", WindowName+"X",      str(screens[backglassScreen]["x"]))
                vpinballSettings.set("Standalone", WindowName+"Y",      str(screens[backglassScreen]["y"]+y))
                vpinballSettings.set("Standalone", WindowName+"Width",  str(width))
                vpinballSettings.set("Standalone", WindowName+"Height", str(height))
        elif vpinball_flexdmd_val=="screen3":
            vpinballSettings.set("Standalone", WindowName,"1")
            vpinballSettings.set("Standalone", WindowName+"X",      str(screens[2]["x"]))
            vpinballSettings.set("Standalone", WindowName+"Y",      str(screens[2]["y"]))
            vpinballSettings.set("Standalone", WindowName+"Width",  str(screens[2]["width"]))
            vpinballSettings.set("Standalone", WindowName+"Height", str(screens[2]["height"]))
        else:
            vpinballSettings.set("Standalone", WindowName,"1")
            if vpinball_flexdmd_val=="flexdmd_topright_small":
                width=small
                x=100-width
            if vpinball_flexdmd_val=="flexdmd_topright_medium":
                width=medium
                x=100-width
            if vpinball_flexdmd_val=="flexdmd_topright_large":
                width=large
                x=100-width
            if vpinball_flexdmd_val=="flexdmd_topleft_small":
                width=small
                x=0
            if vpinball_flexdmd_val=="flexdmd_topleft_medium":
                width=medium
                x=0
            if vpinball_flexdmd_val=="flexdmd_topleft_large":
                width=large
                x=0
            # apply settings
            height=RelativeHeightCalculate(Rscreen,Rwindow,width)
            vpinballSettings.set("Standalone",WindowName+"X",ConvertToPixel(gameResolution["width"],x))
            vpinballSettings.set("Standalone",WindowName+"Y",ConvertToPixel(gameResolution["height"],y))
            vpinballSettings.set("Standalone",WindowName+"Width",ConvertToPixel(gameResolution["width"],width))
            vpinballSettings.set("Standalone",WindowName+"Height",ConvertToPixel(gameResolution["height"],height))

        # B2S and B2SDMD
        WindowName="B2SBackglass"
        Rwindow = 4/3   #Usual Ratio for this window
        # Auto default behaviour is to read values from VPinballX.ini file
        # so we don't do anything in the configgen                    
        if vpinball_b2s_val=="b2s_disabled":
            vpinballSettings.set("Standalone", "B2SWindows","0")
            vpinballSettings.set("Standalone", "B2SHideGrill","1")
        elif vpinball_b2s_val=="screen2":
            vpinballSettings.set("Standalone", "B2SHideGrill","1")
            vpinballSettings.set("Standalone", "B2SWindows","1")
            if vpinball_flexdmd_val=="screen2": # share with flexdmd screen ?
                vpinballSettings.set("Standalone", WindowName,"1")
                vpinballSettings.set("Standalone", WindowName+"X",      str(screens[backglassScreen]["x"]))
                vpinballSettings.set("Standalone", WindowName+"Y",      str(256))
                vpinballSettings.set("Standalone", WindowName+"Width",  str(screens[backglassScreen]["width"]))
                vpinballSettings.set("Standalone", WindowName+"Height", str(screens[backglassScreen]["height"]-256))
            else:
                vpinballSettings.set("Standalone", WindowName,"1")
                vpinballSettings.set("Standalone", WindowName+"X",      str(screens[backglassScreen]["x"]))
                vpinballSettings.set("Standalone", WindowName+"Y",      str(screens[backglassScreen]["y"]))
                vpinballSettings.set("Standalone", WindowName+"Width",  str(screens[backglassScreen]["width"]))
                vpinballSettings.set("Standalone", WindowName+"Height", str(screens[backglassScreen]["height"]))
        else:
            vpinballSettings.set("Standalone", "B2SHideGrill","1")
            vpinballSettings.set("Standalone", "B2SWindows","1")
            if system.config["vpinball_b2s"]=="b2s_topright_small":
                width=small
                x=100-width
            if system.config["vpinball_b2s"]=="b2s_topright_medium":
                width=medium
                x=100-width
            if system.config["vpinball_b2s"]=="b2s_topright_large":
                width=large
                x=100-width
            if system.config["vpinball_b2s"]=="b2s_topleft_small":
                width=small
                x=0
            if system.config["vpinball_b2s"]=="b2s_topleft_medium":
                width=medium
                x=0
            if system.config["vpinball_b2s"]=="b2s_topleft_large":
                width=large
                x=0
            # apply settings
            height=RelativeHeightCalculate(Rscreen,Rwindow,width)
            vpinballSettings.set("Standalone",WindowName+"X",ConvertToPixel(gameResolution["width"],x))
            vpinballSettings.set("Standalone",WindowName+"Y",ConvertToPixel(gameResolution["height"],y))
            vpinballSettings.set("Standalone",WindowName+"Width",ConvertToPixel(gameResolution["width"],width))
            vpinballSettings.set("Standalone",WindowName+"Height",ConvertToPixel(gameResolution["height"],height))
            # B2SDMD
            WindowName="B2SDMD"
            y=height
            Rwindow = 3   #Usual Ratio for this window
            height=RelativeHeightCalculate(Rscreen,Rwindow,width)
            vpinballSettings.set("Standalone",WindowName+"X",ConvertToPixel(gameResolution["width"],x))
            vpinballSettings.set("Standalone",WindowName+"Y",ConvertToPixel(gameResolution["height"],y))
            vpinballSettings.set("Standalone",WindowName+"Width",ConvertToPixel(gameResolution["width"],width))
            vpinballSettings.set("Standalone",WindowName+"Height",ConvertToPixel(gameResolution["height"],height))

        # B2S DMD: not displayed if B2S is hidden
        if system.isOptSet("vpinball_b2sdmd") and system.getOptBoolean("vpinball_b2sdmd") == False: # switchon
            vpinballSettings.set("Standalone", "B2SHideB2SDMD","1")
            vpinballSettings.set("Standalone", "B2SHideDMD","1")
        else:
            vpinballSettings.set("Standalone", "B2SHideB2SDMD","0")
            vpinballSettings.set("Standalone", "B2SHideDMD","0")

        #Sound balance
        if system.isOptSet("vpinball_musicvolume"):
            vpinballSettings.set("Player", "MusicVolume", system.config["vpinball_musicvolume"])
        else:
            vpinballSettings.set("Player", "MusicVolume", "")
        if system.isOptSet("vpinball_soundvolume"):
            vpinballSettings.set("Player", "SoundVolume", system.config["vpinball_soundvolume"])
        else:
            vpinballSettings.set("Player", "SoundVolume", "")
        #Altsound
        if system.isOptSet("vpinball_altsound") and system.getOptBoolean("vpinball_altsound") == False:
            vpinballSettings.set("Standalone", "AltSound", "0")
        else:
            vpinballSettings.set("Standalone", "AltSound","1")

        # DMDServer
        if batoceraServices.isServiceEnabled("dmd_real"):
            vpinballSettings.set("Standalone", "DMDServer","1")
        else:
            vpinballSettings.set("Standalone", "DMDServer","0")

        # Save VPinballX.ini
        with open(vpinballConfigFile, 'w') as configfile:
            vpinballSettings.write(configfile)

        # set the config path to be sure
        commandArray = [
            "/usr/bin/vpinball/VPinballX_GL",
            "-PrefPath", vpinballConfigPath,
            "-Ini", vpinballConfigFile,
            "-Play", rom
        ]

        return Command.Command(array=commandArray, env={"SDL_GAMECONTROLLERCONFIG": controllersConfig.generateSdlGameControllerConfig(playersControllers)})

    def getInGameRatio(self, config, gameResolution, rom):
        return 16/9
