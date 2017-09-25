# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.views.generic.base import View
from django.contrib.auth.models import User
from models import EmailVerifyRecord
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login
from django.shortcuts import render_to_response

class Myapp1Config(AppConfig):
    name = 'myapp1'

class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                username = record.username
                send_type = record.send_type
                if send_type == 'register':
                    user = User.objects.get(username=username)
                    user.is_active = True
                    user.save()
                    login(request, user)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'), {'user': user})

                elif send_type == 'passwd':
                    return render_to_response("myapp1/changepasswd.html", {})
        else:
            return HttpResponse("record fail")

    def post(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            username = all_records[0].username
        else:
            return HttpResponse("record fail")

        new_password = request.POST.get('accPassword', '')
        confirm_new_password = request.POST.get('accPasswordc', '')
        if new_password == confirm_new_password:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return HttpResponse("Congratulations! password modifies success")
        else:
            return HttpResponse('<p>Enter the new password twice inconsistent!</p>')

