# 炉石佣兵战记脚本

## 介绍

本脚本只供学习交流使用，请勿将其商业化或牟利，由此引起的法律后果自负。

欢迎加入我们的QQ群参加测试讨论: 832946624

BUG提交请去 [此页面](https://github.com/zhoubin-me/lushi_script/issues)

## 安装

请确保你安装了python 3.6或以上版本。我们推荐使用 [Anaconda](https://www.anaconda.com/products/individual#windows) 安装python。
请确保你已将python的路径加入到了系统环境变量。

Windows用户请在command line里输入以下来安装需求包：
```bash
pip install opencv-python numpy pyautogui pillow pywin32 pyyaml
```

[comment]: <> (Mac OS 用户请在terminal里输入以下来安装需求包)

[comment]: <> (```bash)

[comment]: <> (pip install opencv-python numpy pyautogui pillow pyyaml psutil PyCocoa)

[comment]: <> (```)


## 运行之前

- 请确保已将你的炉石设为窗口模式
- 英文用户需将炉石分辨率设为 **1024x768**
- 中文用户需将炉石分辨率设为 **1600x900**
- 想要使用其他分辨率，请更改```config_chs.yaml```里的location栏, 用```find_coordinates.py``` 来记录鼠标坐标，并在对应分辨率下截取对应图像来替换```imgs/icons```中的图标
- 开始游戏前，请认真阅读并设置```config.yaml```里的basic和skill栏
- 如果你不想要某些宝藏，请将其对应分辨率下的截图放置```imgs_eng/treasure_blacklist```文件夹
- 如果你想要优先选某些英雄的碎片，请将其对应分辨率下的截图放置```imgs_eng/heros_whitelist```文件夹, **但是**请不要将整个英雄卡牌的图片放进去，只截头像部分即可
- 如果你想让脚本在后台运行，请使用虚拟机
- 请去 [release](https://github.com/zhoubin-me/lushi_script/releases) 页面下载最新的版本，如果你不想要太多bug的话

## 运行

请在你的CMD或者terminal里，cd到```lushi.py```所在文件夹，并运行
```bash
python lushi.py --lang chs
```


