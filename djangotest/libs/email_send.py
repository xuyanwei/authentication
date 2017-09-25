# -*- coding: utf-8 -*-
from random import Random # 用于生成随机码
from django.core.mail import send_mail # 发送邮件模块
from ..settings import EMAIL_HOST_USER  # setting.py添加的的配置信息
from ..myapp1.models import *
import time

# 生成随机字符串
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str


def send_register_email(username, email, send_type="register"):
    try:
        email_record = EmailVerifyRecord()
        code = random_str(16)
        email_record.code = code
        email_record.email = email
        email_record.username = username
        email_record.send_type = send_type
        email_record.save()
        if send_type == "register":
            email_title = "注册激活链接"
            email_body = u"请点击下面的链接激活你的账号:http://127.0.0.1:8081/active/{0}".format(code)
            send_status = send_mail(email_title, email_body, EMAIL_HOST_USER, [email], fail_silently=False)

        elif send_type == "passwd":
            email_title = "修改密码链接"
            email_body = u"请点击下面的链接修改你的密码:http://127.0.0.1:8081/changepassword/{0}".format(code)
            send_status = send_mail(email_title, email_body, EMAIL_HOST_USER, [email], fail_silently=False)

    except Exception, e:
        raise e
