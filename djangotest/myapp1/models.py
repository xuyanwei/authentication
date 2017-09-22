# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
# Create your models here.

class EmailVerifyRecord(models.Model):
    username = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=20, )
    email = models.EmailField(max_length=50,)
    send_type = models.CharField(max_length=10)
    #send_time = models.DateTimeField(default=datetime.datetime.utcnow())
    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return '({0}){1}({2})'.format(self.username, self.code, self.email)
