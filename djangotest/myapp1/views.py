# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response
from models import*
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from ..libs.captcha import *
from ..libs.email_send import *
import re
from PIL import Image

captcha = None

# Create your views here.
def main(request):
    return render_to_response('myapp1/main.html', {'user': request.user})

def sign_up(request):
    global captcha
    if request.method == 'GET':
        captcha = None
        return render_to_response("myapp1/signup.html", {})

    elif request.method == 'POST':
        username = request.POST.get('accName', '')
        passwordi = request.POST.get('accPassWordi', '')
        passwordk = request.POST.get('accPassWordk', '')
        confirm = request.POST.get('accConfirm', '')
        email = request.POST.get('accEmail', '')

        if len(email) < 5 or re.match("[a-zA-Z0-9]+\@+[a-zA-Z0-9]+\.+[a-zA-Z]", email) == None:
            return HttpResponse('邮箱格式有误')

        if captcha.check(confirm):
            if passwordi==passwordk:
                try:
                    user = User.objects.create_user(username=username, password=passwordi)
                    user.is_active = False
                    user.save()
                except Exception, e:
                    return HttpResponse('<p style="font-size:20px">Username already exists! </p>')
                send_register_email(username, email, "register")
                return HttpResponse('<p style="font-size:20px;text-align:center">Congratulations! %s login success, '
                                    'please go to your email(%s) authentication (within 1 hours)</p>' %(username, email))
            else:
                return HttpResponse('<p style="font-size:20px;text-align:center">Enter password twice inconsistent!</p>')
        return HttpResponse('验证码不正确！')

def sign_in(request):
    global captcha
    if request.method == "POST":
        username = request.POST.get('accName', '')
        password = request.POST.get('accPassWord', '')
        confirm = request.POST.get('accConfirm', '')
        if captcha:
            if captcha.check(confirm):
                user = authenticate(username=username, password=password)
                if user is not None:
                    user_login(request, user)
                    return  render_to_response("myapp1/main.html", {'user':request.user})
                else:
                    return HttpResponse('用户名或是密码不正确！')
            return HttpResponse('验证码不正确！')
        return HttpResponse('验证码不存在！请重新访问页面')

    else:
        captcha = None
        #request.session['login_sessionid'] = request.META.get('HTTP_COOKIE', '=').split('=')[1]
        user = request.GET.get('user', '')
        return render_to_response('myapp1/signin.html',{'user':user})

def tmpgif(request):
    global captcha
    _captcha = Captcha(request)
    captcha = _captcha
    return HttpResponse(_captcha.display(), content_type="image/gif")

def sign_out(request):
    user_logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'), {})

def find(request):
    if request.method == "GET":
        return render_to_response('myapp1/find.html', {})
    else:
        username = request.POST.get('accName', '')
        email = request.POST.get('accEmail', '')
        if len(email) < 5 or re.match("[a-zA-Z0-9]+\@+[a-zA-Z0-9]+\.+[a-zA-Z]", email) == None:
            return HttpResponse('邮箱格式有误')
        try:
            User.objects.get(username=username)
        except:
            return HttpResponse('user is not exists')
        send_register_email(username, email, "passwd")
        return HttpResponse("请到您的邮箱验证（1小时之内有效）： （%s）"%email)

def getpassword(request):
    new_password = request.POST.get('password', '')
    confirm_new_password = request.POST.get('c_password', '')
    if new_password == confirm_new_password:
        user = User.objects.get(username=request.user)
        user.set_password(new_password)
        user.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponse('<p>Enter the new password twice inconsistent!</p>')

