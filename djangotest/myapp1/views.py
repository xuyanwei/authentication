# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response

from models import*
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from ..libs.captcha import *
from ..libs.email_send import *
import time,re
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
                return HttpResponse('<p style="font-size:20px;text-align:center">Congratulations! Register is Success, '
                                    'Please go to your email(%s) authentication</p>' % email)
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
                    #return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/successlogin'), {'user': request.user})
                    #return HttpResponseRedirect(request.session['login_from'], {'user': request.user})
                    #return HttpResponse('%s 登录成功！'%user)
                    return  render_to_response("myapp1/main.html", {'user':request.user})
                else:
                    return HttpResponse('用户名或是密码不正确！需要注册邮箱验证')
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

