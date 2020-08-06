#!/usr/bin/python3
# @FileName    :use_mixins_to_optimize_api_view_basis.py
# @Time        :2020/8/6 下午8:59
# @Author      :passerby223
# @Description :

import json
from django.http import Http404
from rest_framework import filters
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend, filterset

from projects.serializer import ProjectModelSerializer
from projects.models import Projects

# 继承GenericAPIView基类，GenericAPIView基类可以提供过滤，排序，分页功能
from utils.custom_pagination import PageNumberPaginationCustom
# 首先继承mixins.ListModelMixin，在继承GenericAPIView，顺序不能乱
class ProjectsList(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   GenericAPIView):
    # 1.指定查询集，queryset用于指定需要使用的查询集
    queryset = Projects.objects.all()
    # 2.指定序列化器，serializer_class指定需要使用到的序列化器类
    serializer_class = ProjectModelSerializer
    # 3.在视图类中指定过滤引擎,也可以在setting.py文件中全局指定过滤引擎，如果全局指定了过滤引擎，这里就不需要再次指定了。
    '''
    DjangoFilterBackend:字段匹配过滤引擎
    OrderingFilter:字段排序过滤引擎
    测试方式：
    浏览器：通过http://127.0.0.1:8000/api/v1/projects/?leader=熊二1格式进行测试
    HTTPie: 通过http -v :8000/api/v1/projects/ ordering==name进行排序测试；
            通过http -v :8000/api/v1/projects/ tester==tester01 developer==developer02进行字段过滤测试
    '''
    # filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    '''
    指定需要过滤的字段
    请求接口http://127.0.0.1:8000/api/v1/projects/?leader=熊二1，返回的是leader=熊二1的项目信息,是全字段匹配，不能匹配字段部分内容
    请求接口http://127.0.0.1:8000/api/v1/projects/?leader=Mike_vip&tester=tester_vip_Jack1，\
    返回的是leader=Mike_vip&tester=tester_vip_Jack1的项目信息,是全字段匹配，不能匹配字段部分内容
    '''
    '''**********特别说明：如果在这里设置了需要做过滤的字段，则在前端中设置的可过滤的字段要跟这里设置的可过滤的字段相同***********'''
    filterset_fields = ['leader', 'tester']
    # 4.指定需要排序的字段,排序功能必须配合过滤引擎才可以正常使用
    '''
    设置排序字段后，启动项目
    请求接口`http://127.0.0.1:8000/api/v1/projects/?ordering=id`，返回的项目列表是以id从小到大进行排序展示的。
    请求接口`http://127.0.0.1:8000/api/v1/projects/?ordering=-id`，返回的项目列表是以id从大到小进行排序展示的。
    如果不设置ordering_fields都有哪些字段，默认是全部字段都加了排序效果。
    如果设置了部分字段加排序效果，则未设置排序效果的字段就不会有排序效果
    '''
    # ordering_fields = ['id', 'name', 'leader']
    '''
    使用lookup_field类属性，可以修改主键路由名称(就是api路径参数中的pk值，默认为pk，可以使用该属性进行覆盖。)
    如果修改了，路径参数也得同步更新
    '''
    # lookup_field = 'id'
    '''
    在单个视图中指定自定义分页类PageNumberPaginationCustom，对其他视图类无效
    '''
    # pagination_class = PageNumberPaginationCustom
    def get(self, request, *args, **kwargs):
        '''
        获取所有项目(可选根据字段进行排序、过滤、分页操作)
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        '''
        第①种情况：设置过滤条件并设置分页
        因为setting.py文件中设置了分页的page个数为1页3条数据，数据库中tester=tester01的数据一共有5条
        浏览器中通过: http://localhost:8000/api/v1/projects/?page=1&tester=tester01 来测试分页效果
        通过httPie请求接口: http -v :8000/api/v1/projects/ tester==tester01 page==1来测试分页效果
                           http -v :8000/api/v1/projects/ tester==tester01 page==2来测试分页效果
        第②种情况：不设置过滤条件但设置分页，此时是按照从数据库中获取到的所有project数据列表来进行分页的
        浏览器中通过:http://localhost:8000/api/v1/projects/?page=1 来测试分页效果
                   http://localhost:8000/api/v1/projects/?page=2 来测试分页效果
                   http://localhost:8000/api/v1/projects/?page=3 来测试分页效果
        httPie: http -v :8000/api/v1/projects/ page==1 来测试分页效果
                 http -v :8000/api/v1/projects/ page==2 来测试分页效果
                 http -v :8000/api/v1/projects/ page==3 来测试分页效果
        '''
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        '''
        新建项目
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        return self.create(request, *args, **kwargs)

# 1. 需要继承GenericAPIView基类
class ProjectsDetail(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericAPIView):
    # 2.必须指定queryset和serializer_class类属性
    # queryset用于指定需要使用的查询集
    queryset = Projects.objects.all()
    # serializer_class指定需要使用到的序列化器类
    serializer_class = ProjectModelSerializer

    def get(self, request, *args, **kwargs):
        '''
        获取某个项目的详情
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        '''
        更新某个项目的数据
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        '''
        删除某个项目
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        return self.destroy(request, *args, **kwargs)
