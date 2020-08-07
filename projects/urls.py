#!/usr/bin/python3
# @FileName    :urls.py
# @Time        :2020/7/21 下午11:27
# @Author      :passerby223
# @Description : 子应用路由表

from django.urls import path, include
from rest_framework import routers
from projects.views import ProjectsViewSet

'''
DefaultRouter了解即可
默认路由器扩展了SimpleRouter，但还添加了默认API根视图，并向URL添加了格式后缀模式。
'''
# router = routers.DefaultRouter()
# 1.创建SimpleRouter路由对象
router = routers.SimpleRouter()
# 2.注册路由
# 第一个参数prefix为路由前缀，一般添加为app(应用名)即可
# 第二个参数viewset为视图集，不要加as_view()
router.register(prefix=r'projects', viewset=ProjectsViewSet)

# 子应用路由表
# ①每一个子应用(模块)都会维护一个子路由(当前子应用的路由信息表)
# ②跟主路由表的匹配规则一样，都是从上往下进行匹配
# ③能匹配上，则执行path第二个参数指定的视图函数，匹配不上，则抛出404异常
urlpatterns = [
    # 函数视图路由
    # 此处每个path中第一个参数一般都留空
    # path('', hello),
    # 类视图路由,path()第二个参数为：类视图类名.as_view()
    # path('', ProjectsView.as_view()),
    # `:`左边为路径参数类型转化器，右边为路径参数变量名
    # Django提供了int,slug,uuid路径参数类型转化器
    # path('<int:pk>/', ProjectsView.as_view())
    # path('', ProjectsList.as_view()),
    # path('<int:pk>/', ProjectsDetail.as_view())
    # path('projects/', ProjectsViewSet.as_view({
    #     'get': 'list',
    #     'post': 'create',
    # }), name='projects-list'),
    # path('projects/<int:pk>/', ProjectsViewSet.as_view({
    #     'get': 'retrieve',
    #     'put': 'update',
    #     'delete': 'destroy',
    # })),
    # path('projects/names/', ProjectsViewSet.as_view({
    #     'get': 'names',
    # }), name='projects-names'),
    # path('projects/<int:pk>/interfaces/', ProjectsViewSet.as_view({
    #     'get': 'interfaces',
    # })),
    # 3.自动生成路由方法①在urlpatterns列表中声明
    # 将自动生成的路由，添加到urlpatterns中
    path('', include(router.urls)),
]
# 3.自动生成路由方法②
# 将自动生成的路由，添加到urlpatterns中
# urlpatterns += router.urls
