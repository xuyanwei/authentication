"""djangotest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from myapp1 import views
from myapp1.apps import ActiveUserView

urlpatterns = [
    url(r'^$', views.main),
    url(r'^tmp/', views.tmpgif),

    url(r'^sign_up/$', views.sign_up),
    url(r'^sign_in/$', views.sign_in),
    url(r'^sign_out/$', views.sign_out),
    url(r'^sign_in/find', views.find),
    url(r'^password/$', views.getpassword),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'^changepassword/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_passwd"),

    url(r'^admin/', admin.site.urls),
]
