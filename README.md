# Sipeed k210 with esp8266
## _Boilerplate_

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

This repository is a boilerplate for starting to work with the k210, here you will find a couple of scripts, all of them are tests basically but are proven to work very good. For the examples I used a esp8266 in the ESP01 shape, connected directly to the Sipeed M1n, no cables needed.

First remove all contents of the esp8266 since I used the serial UART communication, flash the desired firmware depending on the version you have, either the 4MB or 1MB, I used the 1MB version, because it was really old and wanted to prove a point. the commands I used to erase and reflash are these under a ESP-IDF v5 setup.

- esptool.py -p /dev/tty.usbserial-110 erase_flash
- esptool.py -p /dev/tty.usbserial-110 -b 460800 --before default_reset --after hard_reset --chip esp8266  write_flash --flash_mode dout --flash_size 1MB --flash_freq 80m 0x0000 BAT_AT_V1.7.1.0_1M.bin
- ✨Magic ✨

## Reflashing the k210
You will also need to reflash the k210 with the kflash_gui, in such case you need to specify the board that you have and the port. Remember that I used the sipeed M1n, the firmware here, is a backup so that you don't look elsewhere and lose yourself in the way. Download it and flash it.

## Command line utilies needed to work better

You need to use some command line interfaces for better work, this is a list of things that I force you to install

- MaixPy IDE, to watch the camera and program easily in micropython
- mpfs, to work with files directly on the file system, upload, download and run scripts
- ampy, the same as above, but lighter, only to work with text files

## Installation of WIfi
You will need to save the file network_espat.py directly to the board, it will save directly to the "/flash" folder, I do this with the MaixPy IDE, you can use the other tools if needed, the rest of the files afterwards can run without any issues.

Enjoy!