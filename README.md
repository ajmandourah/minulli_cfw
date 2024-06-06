<p align="center">
  <img width="460" height="300" src="https://github.com/ajmandourah/Minulli/assets/27051374/914daa7c-6ca9-4715-a063-038bdbc7e6e8">
</p>

# Minulli
Minulli CFW is a fork of [Knulli](https://github.com/knulli-cfw/distribution) which is a fork of the open-source and completely free retro-gaming distribution batocera that can be copied to an SD card with the aim of improving many of the emulation handhelds on the market that usually ship with incomplete and often non GPL compliant software. It supports [many emulators and game engines](https://www.batocera.org/compatibility.php) out of the box. 
This CFW is mainly aimed toward the Anbrenic RG28xx.

## Why Minulli
Knulli is a great firmware but i felt its a little bit bloated. The aim is to create as minimal batocera as possible removing packages that we don't need and add QoL features from various CFW. 

## Why RG28xx only
The main reason it is what i have in my hands right now. Additionally the number of CFW for this great portable device is scarse so I took the challange and started tinkering around.

## When will you release it
There are several reasons for the slow release:
- My experience in CFW is little in comparision to the legends in the field.
- The compilation time is so long. around 2 hours minimal and 5 if I want to compile everything. you can imagine testing features will take time.
- The RG28xx support is complex.

That aside expect an alpha build soon.


## Directory navigation

 - `board` Platform-specific build configuration. This is where to include special patches/configuration files needed to have particular components work on a particular platform. It is instead encouraged to apply patches at the location of the package itself, but this may not always be possible.
 - `buildroot` Buildroot, the tool used to create the final compiled images. For newcomers, you can safely ignore this folder. Compilation instructions can be found [on the wiki](https://wiki.batocera.org/compile_batocera.linux).
 - `configs` Build flags, which define what components will be built with your image depending on your chose architecture. If you're trying to port Batocera to a new architecture (device, platform, new bit mode, etc.) this is the file you'll need to edit. More information on [the build configuration section on the buildroot compiling page](https://wiki.batocera.org/batocera.linux_buildroot_modifications#define_your_configuration).
 - `package` The "meat and potatoes" of Batocera. This is where the majority of emulator data, config generators, core packages, system utilities, etc. all go into. This is the friendliest place to start dev-work for new devs, as most of it is handled by Python and Makefile.
 - `scripts` Various miscellanous scripts that handle aspects external to Batocera, such as the report data sent to the [compatibility page](https://batocera.org/compatibility.php) or info about the Bezel Project.

A cheatsheet of notable files/folders can be found [on the wiki](https://wiki.batocera.org/notable_files).
