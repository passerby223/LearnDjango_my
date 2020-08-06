from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend, filterset

from projects.serializer import ProjectModelSerializer
from projects.models import Projects

from utils.custom_pagination import PageNumberPaginationCustom


# 首先继承mixins.ListModelMixin，在继承GenericAPIView，顺序不能乱
class ProjectsList(generics.ListCreateAPIView):
    # 1.指定查询集，queryset用于指定需要使用的查询集
    queryset = Projects.objects.all()
    # 2.指定序列化器，serializer_class指定需要使用到的序列化器类
    serializer_class = ProjectModelSerializer
    # 3.在视图类中指定过滤引擎,也可以在setting.py文件中全局指定过滤引擎，如果全局指定了过滤引擎，这里就不需要再次指定了。
    # filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['leader', 'tester']

    # 4.指定需要排序的字段,排序功能必须配合过滤引擎才可以正常使用
    # ordering_fields = ['id', 'name', 'leader']
    # 使用lookup_field类属性，可以修改主键路由名称(就是api路径参数中的pk值，默认为pk，可以使用该属性进行覆盖。)如果修改了，路径参数也得同步更新
    # lookup_field = 'id'
    # 在单个视图中指定自定义分页类PageNumberPaginationCustom，对其他视图类无效
    # pagination_class = PageNumberPaginationCustom


class ProjectsDetail(generics.RetrieveUpdateDestroyAPIView):
    # queryset用于指定需要使用的查询集
    queryset = Projects.objects.all()
    # serializer_class指定需要使用到的序列化器类
    serializer_class = ProjectModelSerializer
