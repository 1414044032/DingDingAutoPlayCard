# DingDingAutoPlayCard
----
钉钉自动上下班打卡辅助
----
新增adb安装文件，可能下载地址有的同学无法访问。
----
4版本基于版本2通过pyinstaller编译为exe文件，只保留了发送邮件功能,只需要安装adb后修改配置文件后，即可使用。不需要依赖python环境。
----
1版本实现自动打卡，邮件提醒。
----
2版本新增短信提醒。通过百度OCR进行文字识别，twilio发送短信，两个版本单独运行。(使用twilio的免费短信实现)
----
3版本新增打卡过程中录像保存到本地的功能，通过线程队列来实现。
----
twilio注册地址[https://www.twilio.com](https://www.twilio.com)
----
基于windows10 ,Python3.6，adb，安卓手机实现。需要安装adb 和python运行环境。原理：通过python逻辑化的调度cmd来执行adb来操作安卓手机。

## 效果展示：
----
![message](https://github.com/1414044032/imgs/blob/master/message1.png)
![daka](https://github.com/1414044032/imgs/blob/master/data.png)
![daka1](https://github.com/1414044032/imgs/blob/master/daka3.png)![daka2](https://github.com/1414044032/imgs/blob/master/daka4.png)
## 1.安装 ADB：
----
windows版本adb下载地址:
[https://adb.clockworkmod.com/](https://adb.clockworkmod.com/)
### 安装完成后，把adb.exe所在文件夹路径加入环境变量Path中。
![1.添加adb到path](https://github.com/1414044032/imgs/blob/master/adbinstall.png)
![2.添加adb到path](https://github.com/1414044032/imgs/blob/master/adbpath.png)
![3.添加adb到path](https://github.com/1414044032/imgs/blob/master/path1.png)
### 手机需要打开开发者选项，通过USB数据线连接电脑。
### 打开CMD命令行，输入“adb devices”,能成功显示手机信息即可。
![cmdshow](https://github.com/1414044032/imgs/blob/master/adbcmd.png)

## 2.安装Python3.6
----
![pythonshow](https://github.com/1414044032/imgs/blob/master/python.png)

## 3.获取屏幕尺寸，设置模拟点击位置：
热心网友提供的简洁方式：可以打开"开发者设置"的输入找到"指针位置" 即可得到点击XY坐标轴。
----
![screen1](https://user-images.githubusercontent.com/40572216/64086339-31f6dc00-cd6a-11e9-9ccd-7ba0ba7624f1.png)
滑动解锁手机。如果手机屏幕自动点亮后不需要解锁。可以在文件中删除滑动解锁的部分。
----
### 像素点的获取：
----
![screen1](https://github.com/1414044032/imgs/blob/master/screen1.png)
![screen2](https://github.com/1414044032/imgs/blob/master/screen2.png)
### 画图工具打开保存到电脑的设备截图：
----
![screen3](https://github.com/1414044032/imgs/blob/master/screen3.png)
![screen4](https://github.com/1414044032/imgs/blob/master/screen4.png)
![screen5](https://github.com/1414044032/imgs/blob/master/screen5.png)

## 4.修改文件参数：
新增配置文件，直接修改配置文件即可
----
![screen6](https://github.com/1414044032/imgs/blob/master/screen6.png)

## 5.运行：
### 定位到文件所在目录。然后执行命令“python DingDing_Secend.py”
----
运行： 'python DingDing_Secend.py'
----
![screen7](https://github.com/1414044032/imgs/blob/master/screen7.png)

## 6.参考资料：
----
[https://github.com/Skyexu/TopSup](https://github.com/Skyexu/TopSup)
----
[https://github.com/mzlogin/awesome-adb](https://github.com/mzlogin/awesome-adb)
----
