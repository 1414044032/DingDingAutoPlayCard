# -*- coding: utf-8 -*-
import subprocess
import time
import sched
import datetime
from io import BytesIO
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

scheduler = sched.scheduler(time.time,time.sleep)
# 上班时间（提前1个小时）也就是8点后打卡，不超过9点
go_hour = 8
# 下班时间 18 -19点中间打卡，不超过19点
back_hour = 18
# adb安装目录
directory = r"D:\Program Files (x86)\ClockworkMod\Universal Adb Driver"
# QQ 邮箱相关
sender = '1414044032@qq.com'  # 发件人邮箱账号
psw = '你的授权码'  # qq邮箱的话是要生成的授权码，其他邮箱类似
receive = '1141962746@qq.com'  # 收件人邮箱账号，我这边发送给自己
# 截屏图片路径（路径不要带空格，为了保存手机发送过来的截屏图片，并保存到邮件中,）
screen_dir = "D:\\screen.png"


# 打开钉钉，关闭钉钉封装为一个妆饰器函数
def with_open_close_dingding(func):
    def wrapper(self, *args, **kwargs):
        print("打开钉钉")
        operation_list = [self.adbpower, self.adbclear, self.adbopen_dingding]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=False,stdout=subprocess.PIPE)
            process.wait()
        # 确保完全启动，并且加载上相应按键
        time.sleep(20)
        print("open dingding success")
        print("打开打卡界面")
        operation_list1 = [self.adbselect_work, self.adbselect_playcard]
        for operation in operation_list1:
            process = subprocess.Popen(operation, shell=False,stdout=subprocess.PIPE)
            process.wait()
            time.sleep(2)
        time.sleep(30)
        print("open playcard success")
        # 包装函数
        func(self, *args, **kwargs)
        print("关闭钉钉")
        operation_list2 = [self.adbback_index, self.adbkill_dingding, self.adbpower]
        for operation in operation_list2:
            process = subprocess.Popen(operation, shell=False,stdout=subprocess.PIPE)
            process.wait()
        print("kill dingding success")
    return wrapper


class dingding:

    # 初始化，设置adb目录
    def __init__(self,directory):
        self.directory = directory
        # 点亮屏幕
        self.adbpower = '"%s\\adb" shell input keyevent 26' % directory
        # 滑屏解锁
        self.adbclear = '"%s\\adb" shell input swipe 300 1000 300 500 500' % directory
        # 启动钉钉应用
        self.adbopen_dingding = '"%s\\adb" shell monkey -p com.alibaba.android.rimet -c android.intent.category.LAUNCHER 1' %directory
        # 关闭钉钉
        self.adbkill_dingding = '"%s\\adb" shell am force-stop com.alibaba.android.rimet'% directory
        # 返回桌面
        self.adbback_index = '"%s\\adb" shell input keyevent 3' % directory
        # 点击工作
        self.adbselect_work = '"%s\\adb" shell input tap 359 1226' % directory
        # 点击考勤打卡
        self.adbselect_playcard = '"%s\\adb" shell input tap 450 893' % directory
        # 点击下班打卡
        self.adbclick_playcard = '"%s\\adb" shell input tap 365 905' % directory
        # 设备截屏保存到sdcard
        self.adbscreencap = '"%s\\adb" shell screencap -p sdcard/screen.png' % directory
        # 传送到计算机
        self.adbpull = '"%s\\adb" pull sdcard/screen.png %s' % (directory,screen_dir)
        # 删除设备截屏
        self.adbrm_screencap = '"%s\\adb" shell rm -r sdcard/screen.png' % directory


    # 点亮屏幕 》》解锁 》》打开钉钉
    def open_dingding(self):
        operation_list = [self.adbpower,self.adbclear,self.adbopen_dingding]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=False,stdout=subprocess.PIPE)
            process.wait()
        # 确保完全启动，并且加载上相应按键
        time.sleep(20)
        print("open dingding success")


    # 返回桌面 》》 退出钉钉 》》 手机黑屏
    def close_dingding(self):
        operation_list = [self.adbback_index,self.adbkill_dingding,self.adbpower]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=False,stdout=subprocess.PIPE)
            process.wait()
        print("kill dingding success")


    # 上班(极速打卡)
    @with_open_close_dingding
    def goto_work(self):
        self.screencap()
        self.sendEmail()
        print("打卡成功")

    # 打开打卡界面
    def openplaycard_interface(self):
        print("打开打卡界面")
        operation_list = [self.adbselect_work, self.adbselect_playcard]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=False,stdout=subprocess.PIPE)
            process.wait()
            time.sleep(2)
        time.sleep(30)
        print("open playcard success")

    # 下班
    @with_open_close_dingding
    def after_work(self):
        operation_list = [self.adbclick_playcard]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=False,stdout=subprocess.PIPE)
            process.wait()
            time.sleep(3)
        self.screencap()
        self.sendEmail()
        print("afterwork playcard success")

    # 截屏>> 发送到电脑 >> 删除手机中保存的截屏
    def screencap(self):
        operation_list = [self.adbscreencap,self.adbpull,self.adbrm_screencap]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=False,stdout=subprocess.PIPE)
            process.wait()
        print("screencap to computer success")

    # 发送邮件（QQ邮箱）
    def sendEmail(self):
        """
        qq邮箱 需要先登录网页版，开启SMTP服务。获取授权码，
        :return:
        """
        now_time = datetime.datetime.now().strftime("%H:%M:%S")
        message = MIMEMultipart('related')
        subject = now_time + '打卡'
        message['Subject'] = subject
        message['From'] = "最疼媳妇的老王"
        message['To'] = receive
        content = MIMEText('<html><body><img src="cid:imageid" alt="imageid"></body></html>', 'html', 'utf-8')
        message.attach(content)
        file = open(screen_dir, "rb")
        img_data = file.read()
        file.close()
        img = MIMEImage(img_data)
        img.add_header('Content-ID', 'imageid')
        message.attach(img)
        try:
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)
            server.login(sender, psw)
            server.sendmail(sender, receive, message.as_string())
            server.quit()
            print("邮件发送成功")
        except smtplib.SMTPException as e:
            print(e)


# 随机打卡时间段
def random_minute():
    return random.randint(30,55)

# 包装循环函数，传入随机打卡时间点
def incode_loop(func,minute):
    """
    包装start_loop任务调度函数，主要是为了传入随机分钟数。保证在不打卡的情况下能保持分钟数不变。
    :param func: star_loop
    :param minute: 随机分钟数
    :return: None
    """
    if datetime.datetime.now().hour <18:
        hourtype = 1
        print("下次将在", str(back_hour), ":", str(minute), "打卡")
    else:
        hourtype = 2
        print("下次将在", str(go_hour), ":", str(minute), "打卡")
    #执行任务调度函数
    func(hourtype,minute)


# 任务调度
def start_loop(hourtype,minute):
    """
    每次循环完成，携带生成的随机分钟数来再次进行循环，当打卡后，再重新生成随机数
    :param hourtype: 设置的上班时间点
    :param minute: 随机生成的分钟数（30-55）
    :return: None
    """
    now_time = datetime.datetime.now()
    now_hour = now_time.hour
    now_minute = now_time.minute
    # 上班，不是周末（双休），小时对应，随机分钟对应
    if hourtype == 2 and now_hour == go_hour and now_minute == minute and is_weekend():
        dingding(directory).goto_work()
        scheduler.enter(0,0,incode_loop,(start_loop,random_minute(),))
    if hourtype == 1 and now_hour == back_hour and now_minute == minute and is_weekend():
        dingding(directory).after_work()
        scheduler.enter(0, 0, incode_loop,(start_loop,random_minute(),))
    else:
        print(now_hour,':',now_minute)
        scheduler.enter(60,0,start_loop,(hourtype,minute,))

# 是否是周末
def is_weekend():
    """
    :return: if weekend return False else return True
    """
    now_time = datetime.datetime.now().strftime("%w")
    if now_time == "6" or now_time == "0":
        return False
    else:
        return True


if __name__ == "__main__":
    # ======formal
    scheduler.enter(0,0,incode_loop,(start_loop,random_minute(),))
    scheduler.run()
    # ====test
    # dingding  = dingding(directory)
    # dingding.goto_work()
    # ==== weekend
    # print(is_weekend())
