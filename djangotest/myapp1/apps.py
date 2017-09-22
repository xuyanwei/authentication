# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.views.generic.base import View
from django.contrib.auth.models import User
from models import EmailVerifyRecord
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login

class Myapp1Config(AppConfig):
    name = 'myapp1'

class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                username = record.username
                user = User.objects.get(username=username)
                user.is_active = True
                user.save()
        else:
            return HttpResponse("active fail")
        login(request, user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'), {'user': user})