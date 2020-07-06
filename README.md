# ZeroSeg

![ZeroSeg on a Raspberry Pi Zero](https://github.com/AverageMaker/Imagestore/blob/master/ZeroSeg-Main_zpsvzs47kds.JPG?raw=true)

A ***improved*** version of code library for the ZeroSeg Raspberry Pi Zero add-on board from [ThePiHut.com](https://thepihut.com/zeroseg).
**This version isn't fully compliant with original ZeroSeg library.** Have been created to simplify
usage of it.

The ZeroSeg contains two (4-character) 7-segment displays, giving you the ability to display
8-digit data on a tiny Pi Zero sized add-on board. It also holds 2 tactile buttons for
controlling data, brightness or any other element of your project.

The ZeroSeg works with any 40 GPIO pin Raspberry Pi – not just the Pi Zero - and is controlled by
a MAX7219CNG integrated circuit, which manages the display of each LED segment, requiring very few
GPIO pins to run the board.

This board’s circuit is wired in the exact same way as generic 7-segment modules, allowing the
use of existing code and libraries to easily create Pi Zero projects with 8-character displays.

This code library was originally cloned from Richard Hull's original open source MAX7219 library
[right here on GitHub](https://github.com/rm-hull/max7219). This has since been replaced with the [luma.led_matrix](https://github.com/rm-hull/luma.led_matrix) library.

## References

[Original base GitHub Repository](https://github.com/rm-hull/max7219) \
[Official ZeroSeg library](https://github.com/AverageMaker/ZeroSeg)

## License

The MIT License (MIT)

Copyright (C) 2016 Richard Hull \
Copyright (C) 2016-2018 Richard Saville \
Copyright (C) 2020 samedamci \<samedamci@disroot.org\>
