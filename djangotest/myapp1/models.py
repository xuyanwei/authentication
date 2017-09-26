# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.

class EmailVerifyRecord(models.Model):
    username = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=50,)
    send_type = models.CharField(max_length=10)
    send_time = models.DateTimeField(default=now())
    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return '({0}){1}({2})'.format(self.username, self.code, self.email)
