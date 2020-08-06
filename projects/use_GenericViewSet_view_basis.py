#!/usr/bin/python3
# @FileName    :use_GenericViewSet_view_basis.py
# @Time        :2020/8/6 下午11:01
# @Author      :passerby223
# @Description :

from rest_framework import filters, status, viewsets
from django_filters.rest_framework import DjangoFilterBackend, filterset
from rest_framework.response import Response

from projects.serializer import ProjectModelSerializer
from projects.models import Projects

from utils.custom_pagination import PageNumberPaginationCustom


class ProjectsViewSet(viewsets.GenericViewSet):
    '''
    如果继承APIView或GenericAPIView的话。下边的方法必须定义为get、post、put、delete等请求方法，这些请求方法全放到一个类中会有冲突。
    所以需要使用viewsets.ViewSet来定义action动作
    ViewSet不支持get、post、put、delete请求方法，只支持action动作
    但是ViewSet中未提供get_object(), get_serializer()等方法(因为ViewSet类不会继承GenericAPIView类)，所以需要继承GenericViewSet类
    '''
    # 1.指定查询集，queryset用于指定需要使用的查询集
    queryset = Projects.objects.all()
    # 2.指定序列化器，serializer_class指定需要使用到的序列化器类
    serializer_class = ProjectModelSerializer
    # 3.在视图类中指定过滤引擎,也可以在setting.py文件中全局指定过滤引擎，如果全局指定了过滤引擎，这里就不需要再次指定了。
    # filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['leader', 'tester']

    # 4.指定需要排序的字段,排序功能必须配合过滤引擎才可以正常使用
    ordering_fields = ['id', 'name', 'leader']
    # 使用lookup_field类属性，可以修改主键路由名称(就是api路径参数中的pk值，默认为pk，可以使用该属性进行覆盖。)如果修改了，路径参数也得同步更新
    # lookup_field = 'id'
    # 在单个视图中指定自定义分页类PageNumberPaginationCustom，对其他视图类无效
    # pagination_class = PageNumberPaginationCustom

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
