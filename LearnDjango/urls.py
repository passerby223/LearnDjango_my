"""LearnDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
# from projects.views import index

# 全局路由表
# 1. urlpatterns为固定名称的列表
# 2. 列表中一个元素就代表一条路由信息
# 3. 从上往下匹配，如果能匹配上,会直接调用path里边的视图方法，如index
# 4. 如果匹配不上，会自动抛出一个404异常
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('index/', index),
    # 这里使用include代表，当在前端访问`http://127.0.0.1:8000/hello/`时，
    # 会从子应用projects的路由表urls文件中去查找对应的路由，执行对应路由绑定的视图方法
    path('hello/', include('projects.urls')),
    # 类视图的父路由
    path('api/v1/projects/', include('projects.urls'))
]
