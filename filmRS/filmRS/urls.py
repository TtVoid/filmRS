"""filmRS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path # 用re_path 需要引入
from django.conf.urls import url

from view import login, nav, main, filmDetail, films

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login.login),
    path('logout/', nav.logout),
    path('main/', main.main),
    path('search/', nav.search),
    path('films/<curPage>', films.films, name='films'),
    path('filmDetail/<id>/<status>/', filmDetail.filmDetail, name='filmDetail'),
    path('filmDetail/<id>/collected/test/', filmDetail.clickCollect, name='clickCollect'),
    path('filmDetail/<id>/rated/<rating>', filmDetail.clickRate, name='clickRate'),
]
