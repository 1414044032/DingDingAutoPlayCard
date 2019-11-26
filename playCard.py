from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess
import time
import setting
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


go_hour = int(setting.go_hour) - 1
back_hour = int(setting.back_hour)
directory = setting.directory
sender = setting.sender
psw = setting.psw
receive = setting.receive
screen_dir = setting.screen_dir


# 打开钉钉以及关闭钉钉封装为一个妆饰器函数
def with_open_close_dingding(func):
    def wrapper(self, *args, **kwargs):
        print("打开钉钉")
        operation_list = [self.adbpower, self.adbopen_dingding]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=False, stdout=subprocess.PIPE)
            process.wait()
        # 确保完全启动，并且加载上相应按键（根据手机响应速度可以调整这里）
        time.sleep(10)
        operation_list1 = [self.adbselect_work, self.adbselect_playcard]
        for operation in operation_list1:
            process = subprocess.Popen(operation, shell=False, stdout=subprocess.PIPE)
            process.wait()
            # 等待点击屏幕后响应
            time.sleep(2)
        # 等待工作页面加载
        time.sleep(30)
        # 执行打卡操作
        func(self, *args, **kwargs)
        print("关闭钉钉")
        operation_list2 = [self.adbback_index, self.adbkill_dingding, self.adbpower]
        for operation in operation_list2:
            process = subprocess.Popen(operation, shell=False, stdout=subprocess.PIPE)
            process.wait()
        print("kill dingding success")

    return wrapper


class dingDing:
    def __init__(self, directory):
        self.directory = directory
        # 点亮屏幕
        self.adbpower = '"%s\\adb" shell input keyevent 26' % directory
        # 滑屏解锁
        # self.adbclear = '"%s\\adb" shell input swipe %s' % (directory, config.light_position)
        # 启动钉钉应用
        self.adbopen_dingding = '"%s\\adb" shell monkey -p com.alibaba.android.rimet -c android.intent.category.LAUNCHER 1' % directory
        # 关闭钉钉
        self.adbkill_dingding = '"%s\\adb" shell am force-stop com.alibaba.android.rimet' % directory
        # 返回桌面
        self.adbback_index = '"%s\\adb" shell input keyevent 3' % directory
        # 点击工作
        self.adbselect_work = '"%s\\adb" shell input tap %s' % (directory, setting.work_position)
        # 点击考勤打卡
        self.adbselect_playcard = '"%s\\adb" shell input tap %s' % (directory, setting.check_position)
        # 点击下班打卡
        self.adbclick_playcard = '"%s\\adb" shell input tap %s' % (directory, setting.play_position)
        # 设备截屏保存到sdcard
        self.adbscreencap = '"%s\\adb" shell screencap -p sdcard/screen.png' % directory
        # 传送到计算机
        self.adbpull = '"%s\\adb" pull sdcard/screen.png %s' % (directory, screen_dir)
        # 删除设备截屏
        self.adbrm_screencap = '"%s\\adb" shell rm -r sdcard/screen.png' % directory

    # 点亮屏幕 》》解锁 》》打开钉钉
    def open_dingding(self):
        operation_list = [self.adbpower, self.adbopen_dingding]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=False, stdout=subprocess.PIPE)
            process.wait()
        # 确保完全启动，并且加载上相应按键
        time.sleep(20)
        print("open dingding success")

    # 返回桌面 》》 退出钉钉 》》 手机黑屏
    def close_dingding(self):
        operation_list = [self.adbback_index, self.adbkill_dingding, self.adbpower]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=False, stdout=subprocess.PIPE)
            process.wait()
        print("kill dingding success")

    # 上班(极速打卡)
    @with_open_close_dingding
    def goto_work(self):
        self.screencap()
        self.send_email()
        print("打卡成功")

    # 打开打卡界面
    def openplaycard_interface(self):
        print("打开打卡界面")
        operation_list = [self.adbselect_work, self.adbselect_playcard]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=False, stdout=subprocess.PIPE)
            process.wait()
            time.sleep(2)
        time.sleep(30)
        print("open playcard success")

    # 下班
    @with_open_close_dingding
    def off_work(self):
        operation_list = [self.adbclick_playcard]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=False, stdout=subprocess.PIPE)
            process.wait()
            time.sleep(3)
        self.screencap()
        self.send_email()
        print("afterwork playcard success")

    # 截屏>> 发送到电脑 >> 删除手机中保存的截屏
    def screencap(self):
        operation_list = [self.adbscreencap, self.adbpull, self.adbrm_screencap]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=False, stdout=subprocess.PIPE)
            process.wait()
        print("screencap to computer success")

    # 发送邮件（QQ邮箱）
    @staticmethod
    def send_email():
        """
        qq邮箱 需要先登录网页版，开启SMTP服务。获取授权码，
        :return:
        """
        now_time = datetime.datetime.now().strftime("%H:%M:%S")
        message = MIMEMultipart('related')
        subject = now_time + '打卡'
        message['Subject'] = subject
        message['From'] = "日常打卡"
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


def job1():
    print("开始打卡")
    dingDing(directory).goto_work()


def job2():
    print("开始打卡")
    dingDing(directory).off_work()


# BlockingScheduler
if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(job1, 'cron', day_of_week='1-5', hour=go_hour, minute=38)
    scheduler.add_job(job2, 'cron', day_of_week='1-5', hour=back_hour, minute=2)
    scheduler.start()
    # dingDing(directory).open_dingding()
