# lushi_script


## Introduction
This script is to save your time from Mercenaries mode of Hearthstone.
Currently only support H1-2 map.

### Update
* Support selection of heros
* Use config files
* Support early stop once collected rewards from stranger
* Fixed problem caused by ice wall from rewards
* Fixed problem caused by blue portal, boom, etc
* Support more maps with different count of rewards

### Plan
* Support English
* Support more resolution
* Support multi-round battle skill selection

### Caution
- Currently only support Simplified Chinese
- Make sure you save your ```config.txt``` in 'utf-8' format

## Installation

Make sure you installed python>=3.6.
To install python, we recommand [Anaconda](https://www.anaconda.com/products/individual#windows).
Make sure you added python path into your ```$PATH``` system environment/variables

Run the following in your commandline/terminal
```bash
pip install opencv-python numpy pyautogui pillow pywin32
```

## Run
If you need stable version, goto Release to download.
If you wanna test latest version, download the main branch.

In your commandline/terminal, CD to ```lushi_script``` folder,  run the following
```bash
python lushi.py 
```
