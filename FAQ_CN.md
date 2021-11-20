## 小白常见问题

Q:我完全没学过代码能用这个脚本吗？  
A:完全没问题，英语不要太差，善用百度能解决大部分问题。  


### 1.运行pip intall指令时的常见问题

Q：这些东西下载来有什么用？  
A：这些是脚本运行时的依赖库，不可或缺。  

Q:在cmd中运行pip install指令时跳出黄字警告怎么办  
A:这个是正常现象不需要管。  

Q:在cmd中运行pip install指令时出现一长串的红色字符怎么办？  
A：说明下载失败了，尝试多运行几次pip install指令，直到全部显示Requirement already satisfied既可。

Q: 在cmd中运行pip install指令时显示 'pip' 不是内部或外部命令，也不是可运行的程序或批处理文件是为什么？  
A：说明你没安装Python，可以直接百度python官网或者去微软商店里面下载。  

Q: psutil依赖包下载完成后显示安装失败了,重试了好几次还是一样是为什么？  
A: 说明你安装的Python版本过高，可以下载[Micsoft Visaul C++](https://download.visualstudio.microsoft.com/download/pr/d3cbdace-2bb8-4dc5-a326-2c1c0f1ad5ae/9B9DD72C27AB1DB081DE56BB7B73BEE9A00F60D14ED8E6FDE45DAB3E619B5F04/VC_redist.x64.exe)后再次运行指令即可,也可以直接重新安装旧版的Python 3.7 或者Python 3.8  

Q:下载速度实在是太慢了，有没有什么解决办法？  
A:可以尝试使用运行以下指令来运行  
```pip install -r requirements.txt -i https://pypi.douban.com/simple/```

Q: 出现ModuleNotFoundError: No Module named 'hearthstone'怎么办
A: 依赖包安装缺失，请运行文件夹下的install.bat

Q: 出现 ImportError: DLL load failed while importing win32api: 找不到指定的模块怎么办
A: [查看该回答](https://blog.csdn.net/qq_36834256/article/details/105870593)


### 2.安装相关软件的注意事项-
Q: 安装Python时有什么要注意的？  
A: 如果没有特殊需求强烈建议安装Python 3.7或者Python 3.8版本，建议使用微软商店或者去Python官网下载安装。  

Q: 安装[Anaconda3](https://www.anaconda.com/products/individual#windows)时有什么需要注意的？  
A: 安装时请仔细看清每一步，确保在Advanced Options界面时勾选Add Anaconda3 to the system PATH environment variable选项（该选项默认是不勾选的）以确保脚本的正常运行。  


### 3.如何运行脚本的相关问题
Q: 上面的这些步骤我已经全部完成了，脚本压缩包也下载并解压好了，为什么我双击lushi.py没有任何反应？  
A：旧版本适用：~~lushi.py没有办法直接运行，需要通过cmd启动。如果你安装了Anaconda，可以通过启动Anaconda Prompt来打开命令行。比如，你下载的本项目的路径为```C:\\Users\\Downloads\\lushi_script```,
则在命令行中输入```cd C:\\Users\\Downloads\\lushi_script```，按回车到当前目录，再输入```python lushi.py```回车即可启动脚本。具体的操作方法为在cmd中输入CD加空格加lushi.py所在路径，详细可参照[命令提示符——CMD目录操作——cd命令]~(https://jingyan.baidu.com/article/73c3ce28480637e50343d992.html)。 

新版本适用：双击start_gui.bat

Q: 成功启动脚本后该如何设置脚本？  
A: ~~旧版本适用：脚本的设置文件是config_chs.yaml和config_eng.yaml这两个文件，根据你炉石客户端的语言设置对应的配置文件即可~~

   现版本可直接通过GUI修改和导入设置，为了正常运行，必须要修改战网路径和炉石路径，部分版本在启动前必须要先保存才能使配置生效，另外，将设置保存成default.yaml可以在下次打开自动导入，

  

### 4.Power.log相关问题

Q: 为什么脚本一到上佣兵环节就不动了

A: 检查配置中的炉石路径是否正确，并检查炉石路径下的Logs文件夹里面是否有Power.log文件


Q: 我没有找到Power.log文件怎么办

A1: Power.log一旦游戏战斗开始就会自动出现，所以只要你炉石路径填对了，脚本就能正常运行。

A2: 如果你在Logs/目录下没有找到Power.log（指对战开始后），可以先用记牌器软件（HDT，炉石官方助手，炉石盒子）启动一次炉石传说，以后就会自动生成。

A2: 如果你不想下载记牌器软件，那稍微有一些麻烦。你需要到C:\Users\你的用户\AppData\Local\Blizzard\Hearthstone目录下新建一个叫log.config的文件（如果已经有就不用新建了），然后把下面这段代码放进去（如果已经有[Power]相关则更改相关设置）:
```yaml
[Power]
LogLevel=1
FilePrinting=True
ConsolePrinting=False
ScreenPrinting=False
Verbose=True
```

关于炉石log的更多信息可以查看这个 [Reddit帖子](https://www.reddit.com/r/hearthstone/comments/268fkk/simple_hearthstone_logging_see_your_complete_play/) 。


### 5.奇怪问题，例如莫名其妙退出
Q: 为啥闪退?为啥不动?为啥...?

A: 需要查看报错信息，如果你的版本有log文件夹，可以通过他查看历史状态，如果无该文件，可以把main_gui.bat后缀名编辑为txt然后把文件中的pythonw修改为python，再把后缀名改为bat运行查看报错信息

### 6.platform初始化错误
Q: 出现如下错误

![image](https://user-images.githubusercontent.com/46051884/141449319-11fddc54-546d-4742-bf39-e533ab9d652f.png)

A: 查看文件路径，避免中文路径

### 7.电脑/游戏不支持对应分辨率
Q: 无法选择1600*900分辨率

A：可以参考https://github.com/zhoubin-me/lushi_script/issues/131#issuecomment-966912310

### 8.卡营火

由于连续点击地图会拖动导致，可以修改default.yaml中的delay
![image](https://user-images.githubusercontent.com/46051884/142219998-f2626f5c-47c3-4550-a80d-86d65a367c77.png)


### 9.总结不上怪

依次排查 power.log是否能正确生成, 炉石战网路径是否正确 


### 10.can not get name of process psutil.AccessDenied (pid=1804)

请使用管理员权限打开脚本


### 11 启动程序出现 raise assertionerror()
需要删除power.log重新进入游戏
