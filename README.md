<p align="center">
  <img src="https://github.com/ajmandourah/minulli_cfw/assets/27051374/e15b1fdb-64ad-45a4-9780-fa48a6725358">
</p>


# Minulli
Minulli CFW is a fork of [Knulli](https://github.com/knulli-cfw/distribution) which is a fork of the open-source and completely free retro-gaming distribution batocera that can be copied to an SD card with the aim of improving many of the emulation handhelds on the market that usually ship with incomplete and often non GPL compliant software. It supports [many emulators and game engines](https://www.batocera.org/compatibility.php) out of the box.
This CFW is mainly aimed toward the Anbrenic RG28xx.

## Why Minulli
Knulli is a great firmware but i felt its a little bit bloated. The aim is to create as minimal batocera as possible removing packages that we don't need and add QoL features from various CFW.

Most of us already tried the stock firmware and in that time you get used to it. especially the mappings and the features. Transitioning to a CFW will confuse most of people especially when it comes to batocera. Thats why I intend to implement stock features and implement its mapping for the ease of use. of course these are customizable if you wish to do so afterwords.

## Features

<p align="center">
  <img width="300" src="https://github.com/ajmandourah/minulli_cfw/assets/27051374/1586b91c-c162-4f39-881b-a37677f49c42">    <img width="300" src="https://github.com/ajmandourah/minulli_cfw/assets/27051374/dc52f526-15c9-43d2-a1a2-4a24444878ea">
</p>

Minulli aim to appeal to the general normal non-advanced users who want to uses Batocera without extra work to do , The aim is to get a close to stock experience + additional features. this will include the following:

- ExFat partition by default. This will allow windows users to directly copy all roms and bios without the need to format/expand the partition.
- Minulli relies on Retroarch most of the time. all roms will be launched using retroarch cores. Exception for some systems like NDS where drastic is the default emulator etc.
- included standalone emulators are drastic and ppsspp (Additional standalone emulator will be included if the community wish so)
- Retroarch mapping that is similar to the stock firmware.
- Quick save and shutdown and restore last game on start implemented. more information below.
- Custom simple theme added. with the ability to download other themes if you wish so .
- Wireless connection is supported. you need a USB c to A dongle and a usb wireless stick.

## Shutdown and suspend reworks. Save on exit. 
There have been several efforet from the knulli team to address some issues. in addition to the added feature of Save on exit from stock . 
- light press on the power button will **Suspend the device** unless you are in a game powered by RA core where it will **shutdown and save.**
- Long press will always **shutdown** . you will get a nice haptic feedback when doing so . 
- when powering on your device if a save on shutdown has been down . you will automaticlly start from where you left.
  
## Why RG28xx only
The main reason it is what i have in my hands right now. Additionally the number of CFW for this great portable device is scarse so I took the challange and started tinkering around.

## Why the slow release interval:
There are several reasons for the slow release:
- My experience in CFW is little in comparision to the legends in the field.
- The compilation time is so long. around 2 hours minimal and 5 if I want to compile everything. you can imagine testing features will take time.
- The RG28xx support is complex.

## Todo
- ~Shrink down the image size~
- ~Implement quick save before shutdown script and a load after startup~
- Simplify menu tree
- ~remap retroarch button to match stock firmware~
- remap menu button in batocera to start menu

## Download and Install
You can see all the releases in the release section https://github.com/ajmandourah/minulli_cfw/releases
- Backup your roms and saves
- Download the image from https://github.com/ajmandourah/minulli_cfw/releases
- Flash the image using your favourite image burning program. I use Rufus https://rufus.ie/en/
- Insert the SD card after flashing to your RG28xx. wait for the first boot.
- After booting succesfully shutdown your device. Take out your SD card and insert it into your PC. Add your roms and saves accordingly.
- EnJoY

## Directory navigation

 - `board` Platform-specific build configuration. This is where to include special patches/configuration files needed to have particular components work on a particular platform. It is instead encouraged to apply patches at the location of the package itself, but this may not always be possible.
 - `buildroot` Buildroot, the tool used to create the final compiled images. For newcomers, you can safely ignore this folder. Compilation instructions can be found [on the wiki](https://wiki.batocera.org/compile_batocera.linux).
 - `configs` Build flags, which define what components will be built with your image depending on your chose architecture. If you're trying to port Batocera to a new architecture (device, platform, new bit mode, etc.) this is the file you'll need to edit. More information on [the build configuration section on the buildroot compiling page](https://wiki.batocera.org/batocera.linux_buildroot_modifications#define_your_configuration).
 - `package` The "meat and potatoes" of Batocera. This is where the majority of emulator data, config generators, core packages, system utilities, etc. all go into. This is the friendliest place to start dev-work for new devs, as most of it is handled by Python and Makefile.
 - `scripts` Various miscellanous scripts that handle aspects external to Batocera, such as the report data sent to the [compatibility page](https://batocera.org/compatibility.php) or info about the Bezel Project.

A cheatsheet of notable files/folders can be found [on the wiki](https://wiki.batocera.org/notable_files).
