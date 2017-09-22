# coding=utf-8
from django.http import HttpResponse

from . import Captcha


def show_captcha(request):
    #return Captcha(request).display()
    return HttpResponse(Captcha(request).display(), content_type="image/gif")
