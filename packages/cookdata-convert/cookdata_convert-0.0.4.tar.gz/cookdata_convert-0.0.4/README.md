# Breath of the Wild CookData Convert
Converts CookData (cooking recipes) from machine code to human-readable format and replaces hashed names with strings (or vice versa). For LoZ:BotW

## Dependencies
* A dumped copy of Legend of Zelda: Breath of the Wild (for Wii U or Switch)
* Python 3.7+ (64-bit, added to system PATH)

The following `pip` packages, which will be automatically installed:
* oead

## Setup
1. Download and install Python 3.7+, 64-bit. You must choose the "Add to System PATH" option during installation.
2. Open a command line and run `pip install cookdata_convert`

### How to Use
First, navigate to the folder that contains the CookData, then run one or both of the following functions.

#### Convert CookData.sbyml to YAML:
```cookdata_convert yml```
* `yml` can be replaced with `y`

#### Convert CookData.yml to SBYML:
```cookdata_convert sbyml [-b]```
* `sbyml` can be replaced with `s`
* `-b` - Use big-endian mode. For deleting flags for Wii U.

## Contributing
* Issues: https://github.com/GingerAvalanche/cookdata_convert/issues
* Source: https://github.com/GingerAvalanche/cookdata_convert

This software is in early, but usable, beta. There are several variable types that are not yet handled, and several cases that are not handled for the variable types that are handled. Feel free to contribute in any way.

## License
This software is licensed under the terms of the GNU Affero General Public License, version 3+. The source is publicly available on Github.
