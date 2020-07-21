#!/usr/bin/python3
# @FileName    :urls.py
# @Time        :2020/7/21 下午11:27
# @Author      :passerby223
# @Description : 子应用路由表

from django.urls import path
from projects.views import hello

# 子应用路由表
# 1. 每一个子应用(模块)都会维护一个子路由(当前子应用的路由信息表)
# 2. 跟主路由表的匹配规则一样，都是从上往下进行匹配
# 3. 能匹配上，则执行path第二个参数指定的视图函数，匹配不上，则抛出404异常
urlpatterns = [
    # 此处每个path中第一个参数一般都留空
    path('', hello)
]
