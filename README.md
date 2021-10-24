# lushi_script


## Introduction
This script is to save your time from Mercenaries mode of Hearthstone. 

It is only for study purpose, you will take your own legal responsibility if you commercialize it or earn profit.

For discussion, welcome to our QQ Group: 832946624

### Update
* Support selection of heros
* Use YAML config file
* Support early stop once collected rewards from stranger
* Fixed problem caused by ice wall from rewards
* Fixed problem caused by blue portal, boom, etc
* Fixed surprise location caused hangs
* Fixed hero selection problem of team size 3, 4, 5
* Support more maps with different count of rewards
* Support multi-round battle skill selection

### Plan
* Support English
* Support more resolution
* Support enemy and hero count
* Support Mac/Linux

### Caution
- Currently only support Simplified Chinese
- If you wanna blacklist some treasures during selection, put their screenshot into treasure_blacklist
- Please download to lastest stable version in release page, if you still have problems, please report on issues page
- For more resolutions, change locations in ```config.yaml```, use ```find_coordinates.py``` to record button locations
- Please read carefully about basic section and skill section in  ```conig.yaml``` before you start your game
## Installation

Make sure you installed python>=3.6.
To install python, we recommand [Anaconda](https://www.anaconda.com/products/individual#windows).
Make sure you added python path into your ```$PATH``` system environment/variables

Run the following in your commandline/terminal for requirements installation
```bash
pip install opencv-python numpy pyautogui pillow pywin32 pyyaml
```

## Run
If you need a stable version, goto Release to download.
If you wanna test latest version, download the main branch.

In your commandline/terminal, CD to folder where ```lushi.py``` locates,  run the following
```bash
python lushi.py 
```
