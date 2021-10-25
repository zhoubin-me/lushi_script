# lushi_script


## Introduction
This script is to save your time from Mercenaries mode of Hearthstone. 

It is only for study purpose, you will take your own legal responsibility if you commercialize it or earn profit.

For discussion, welcome to our QQ Group: 832946624

For bug reporting, please go to issues page to submit

### Update
* Support selection of heros
* Use YAML config file
* Support early stop once collected rewards from stranger
* Fixed problem caused by ice wall from rewards
* Fixed problem caused by blue portal, boom, etc
* Fixed surprise location caused hangs
* Fixed hero selection problem of team size 3, 4, 5
* Fixed problem of re-entering battle mode when boom is met and surrender
* Support more maps with different count of rewards
* Support multi-round battle skill selection

### Plan
* Support English
* Support more resolution
* Support enemy and hero count
* Support Mac/Linux

## Installation

Make sure you installed python>=3.6.
To install python, we recommand [Anaconda](https://www.anaconda.com/products/individual#windows).
Make sure you added python path into your ```$PATH``` system environment/variables

Run the following in your commandline/terminal for **Requirements** installation
```bash
pip install opencv-python numpy pyautogui pillow pywin32 pyyaml
```

## Caution
- Currently only support **Simplified Chinese**, make sure your Hearthstone language is set to this
- Default **resolution** is 1600x900 in windows mode; for more resolutions, change locations in ```config.yaml```, use ```find_coordinates.py``` to record button locations
- Please read carefully about **basic section and skill section** in  ```conig.yaml``` before you start your game
- If you wanna blacklist some treasures during selection, put their screenshot into ```treasure_blacklist``` folder
- If you wanna run it in background, consider using a virtual machine
- Please download to **lastest stable** version in release page, if you still have problems, please report on issues page

## Run
If you need a stable version, goto Release to download.
If you wanna test latest version, download the main branch.

In your commandline/terminal, CD to folder where ```lushi.py``` locates,  run the following
```bash
python lushi.py 
```
