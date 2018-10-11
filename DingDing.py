# -*- coding: utf-8 -*-
import subprocess
import time
import sched
import datetime
from io import BytesIO
import random

scheduler = sched.scheduler(time.time,time.sleep)
# 上班时间
go_hour = 8
# 下班时间
back_hour = 19
# adb安装目录
directory = r"D:\Program Files (x86)\ClockworkMod\Universal Adb Driver"

# 打开钉钉，关闭钉钉封装为一个妆饰器函数
def with_open_close_dingding(func):
    def wrapper(self, *args, **kwargs):
        print("打开钉钉")
        operation_list = [self.adbpower, self.adbclear, self.adbopen_dingding]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=False)
            process.wait()
        # 确保完全启动，并且加载上相应按键
        time.sleep(20)
        print("open dingding success")
        print("打开打卡界面")
        operation_list1 = [self.adbselect_work, self.adbselect_playcard]
        for operation in operation_list1:
            process = subprocess.Popen(operation, shell=False)
            process.wait()
            time.sleep(2)
        time.sleep(30)
        print("open playcard success")
        # 包装函数
        func(self, *args, **kwargs)
        print("关闭钉钉")
        operation_list2 = [self.adbback_index, self.adbkill_dingding, self.adbpower]
        for operation in operation_list2:
            process = subprocess.Popen(operation, shell=False)
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


    # 点亮屏幕 》》解锁 》》打开钉钉
    def open_dingding(self):
        operation_list = [self.adbpower,self.adbclear,self.adbopen_dingding]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=True)
            process.wait()
        # 确保完全启动，并且加载上相应按键
        time.sleep(20)
        print("open dingding success")


    # 返回桌面 》》 退出钉钉 》》 手机黑屏
    def close_dingding(self):
        operation_list = [self.adbback_index,self.adbkill_dingding,self.adbpower]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=True)
            process.wait()
        print("kill dingding success")


    # 上班(极速打卡)
    @with_open_close_dingding
    def goto_work(self):
        print("打卡成功")

    # 打开打卡界面
    def openplaycard_interface(self):
        print("打开打卡界面")
        operation_list = [self.adbselect_work, self.adbselect_playcard]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=False)
            process.wait()
            time.sleep(2)
        time.sleep(30)
        print("open playcard success")

    # 下班
    @with_open_close_dingding
    def after_work(self):
        operation_list = [self.adbclick_playcard]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=True)
            process.wait()
            time.sleep(3)
        print("afterwork playcard success")


def random_minute():
    return random.randint(35,55)

# 包装循环函数
def incode_loop(func,minute):
    func(minute)


# 任务调度
def start_loop(minute):
    print(minute)
    now_time = datetime.datetime.now()
    now_hour = now_time.hour
    now_minute = now_time.minute
    if now_hour == go_hour and now_minute == minute:
        dingding(directory).goto_work()
        scheduler.enter(0,0,incode_loop,(start_loop,random_minute(),))
    if now_hour == back_hour and now_minute == minute:
        dingding(directory).after_work()
        scheduler.enter(0, 0, incode_loop,(start_loop,random_minute(),))
    else:
        print(now_hour,':',now_minute)
        scheduler.enter(3,0,start_loop,(minute,))



if __name__ == "__main__":
    scheduler.enter(0,0,incode_loop,(start_loop,random_minute(),))
    scheduler.run()

