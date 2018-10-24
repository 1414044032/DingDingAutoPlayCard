# -*- coding: utf-8 -*-
from aip import AipOcr
import io
from twilio.rest import Client
import configparser
from PIL import Image

config = configparser.ConfigParser(allow_no_value=False)
config.read("dingding.cfg")
screen_dir = config.get("screen","screen_dir")
class SendMessage:

    def __init__(self,hourtype):
        self.hourtype = hourtype
        self.screen_dir = screen_dir

    # 截取上班图片
    def TailorImage(self,path):
        img = Image.open(path)
        # 上班位置
        if self.hourtype == 2:
            box = (58, 347, 655, 602)
        else:
            box = (130, 597, 560, 900)
        taimg = img.crop(box)
        return taimg

    # 百度文本识别
    def baidu_img_str(self,image):
        APP_ID = "11660670"
        API_KEY = "RG8QR4q9pgow4qyY3FhUFRFD"
        SECRET_KEY = "1MKLlb2GvvKEAD8Hjo9M8PYwdiQL8EyU"
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        image_data = img_byte_arr.getvalue()
        # base64_data = base64.b64encode(image_data)
        response = client.basicGeneral(image_data)
        print(response)
        result = []
        for i in response.get("words_result")[0:2]:
            result.append(i.get('words'))
        return ",".join(result)

    # 发送短信(twilio)
    def Send(self,shotmessage):
        account = config.get("twilio", "account")
        token = config.get("twilio", "token")
        client = Client(account, token)
        body = shotmessage
        try:
            message = client.messages.create(to=config.get("twilio", "to"), from_=config.get("twilio", "from"),
                                             body=body)
            print("短信状态",message.status)
            return shotmessage
        except Exception as e:
            return shotmessage

    def PlayCardSendMessage(self):
        image = self.TailorImage(self.screen_dir)
        shotmessage = self.baidu_img_str(image)
        self.Send(shotmessage)
        return shotmessage