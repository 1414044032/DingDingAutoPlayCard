# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request

from common.Helper import ops_render
import subprocess
import base64
import os

route_index = Blueprint('index_page', __name__)


@route_index.route("/")
def index():
    return ops_render("index/index.html")


@route_index.route("/testAdb")
def test_adb():
    abs_adbpath = request.args.get("adbpath")
    cmd = '"%s\\adb" devices' % abs_adbpath
    print(cmd)
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        process.stdout.flush()
        result = b""
        for line in iter(process.stdout.readline, b''):
            result = result + line
        print(result)
        process.stdout.close()
        return jsonify({"name": result.decode('utf-8')})
    except Exception:
        return jsonify({"name": "error"})


@route_index.route("/getimg")
def getimg():
    abs_adbpath = request.args.get("adbpath")
    screen_dir = request.args.get("screen_dir") + "\screen.jpg"
    cmd = '%s\\adb shell screencap -p sdcard/screen.jpg' % abs_adbpath
    cmd1 = '%s\\adb pull sdcard/screen.jpg %s' % (abs_adbpath, screen_dir)
    print(cmd)
    print(cmd1)
    try:
        process = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE)
        process.wait()
        process1 = subprocess.Popen(cmd1, shell=False, stdout=subprocess.PIPE)
        process1.wait()
        if os.path.exists(screen_dir):
            with open(screen_dir, "rb") as f:
                # b64encode是编码，b64decode是解码
                base64_data = base64.b64encode(f.read())
                # base64.b64decode(base64data)
                print(base64_data)
            return jsonify({"name": "data:image/jpg;base64," + base64_data.decode('utf-8')})
        else:
            return jsonify({"name": ""})
    except Exception as e:
        print(e)
        return jsonify({"name": ""})


@route_index.route("/createseting", methods=["POST"])
def createseting():
    try:
        form = request.form.to_dict()
        go_hour = form["go_hour"]
        back_hour = form["back_hour"]
        psw = form["psw"]
        receive = form["receive"]
        sender = form["sender"]
        screen_dir = form["screen_dir"]
        work_position = form["work_position"]
        check_position = form["check_position"]
        play_position = form["play_position"]
        input = form["input"]
        insert_word = """# adb install path
    directory = "{input}"
    #  go work time  if you are 9  here need  add 8
    go_hour = {go_hour}
    # back work time if you are 18 here need add 18
    back_hour = {back_hour}
    # send person
    sender = "{sender}"
    # password  Generally, third party login is required authorization code
    psw = "{psw}"
    # recevie  here It could be yourself
    receive = "{receive}"
    
    # Screen shot image path (do not include Spaces in the path, in order to save the screen shot sent by the phone, and save it in the email)
    screen_dir = "{screen_dir}"
    # Touch the screen on a series of coordinates.
    # Slide to unlock
    light_position = "300 1000 300 500"
    # Click "work"
    work_position = "{work_position}"
    # Click "time check"
    check_position = "{check_position}"
    # Click on "off duty"
    play_position = "{play_position}"
    """
        last_word = insert_word.format(**form)
        print(last_word)
        print(last_word)
        with open("setting.py", "w") as file:
            file.write(last_word)
        return jsonify({"name": "success"})
    except Exception as e:
        print(e)
        return jsonify({"name": ""})
