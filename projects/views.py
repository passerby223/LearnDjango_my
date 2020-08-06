from rest_framework import filters, viewsets, mixins
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend, filterset
from rest_framework.response import Response

from projects.serializer import ProjectModelSerializer, ProjectNameModelSerializer
from projects.models import Projects

from utils.custom_pagination import PageNumberPaginationCustom


# class ProjectsViewSet(mixins.ListModelMixin,
#                       mixins.CreateModelMixin,
#                       mixins.UpdateModelMixin,
#                       mixins.RetrieveModelMixin,
#                       mixins.DestroyModelMixin,
#                       viewsets.GenericViewSet):
class ProjectsViewSet(viewsets.ModelViewSet):
    '''
    如果继承APIView或GenericAPIView的话。下边的方法必须定义为get、post、put、delete等请求方法，这些请求方法全放到一个类中会有冲突。
    所以需要使用viewsets.ViewSet来定义action动作
    ViewSet不支持get、post、put、delete请求方法，只支持action动作
    但是ViewSet中未提供get_object(), get_serializer()等方法(因为ViewSet类不会继承GenericAPIView类)，所以需要继承GenericViewSet类
    '''
    # 1.指定查询集，queryset用于指定需要使用的查询集
    queryset = Projects.objects.all().order_by('id')
    # 2.指定序列化器，serializer_class指定需要使用到的序列化器类
    serializer_class = ProjectModelSerializer
    # 3.在视图类中指定过滤引擎,也可以在setting.py文件中全局指定过滤引擎，如果全局指定了过滤引擎，这里就不需要再次指定了。
    # filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['name', 'leader', 'tester']

    # 4.指定需要排序的字段,排序功能必须配合过滤引擎才可以正常使用
    # ordering_fields = ['id', 'name', 'leader']

    # 使用lookup_field类属性，可以修改主键路由名称(就是api路径参数中的pk值，默认为pk，可以使用该属性进行覆盖。)如果修改了，路径参数也得同步更新
    # lookup_field = 'id'
    # 在单个视图中指定自定义分页类PageNumberPaginationCustom，对其他视图类无效
    # pagination_class = PageNumberPaginationCustom

    @action(methods=['get'], detail=False)
    def names(self, request):
        '''
        获取所有项目的name
        1.可以使用action装饰器来声明自定义action动作，默认情况下，实例方法名就是action动作名
        2.methods参数用于指定该action支持的请求方法，默认是get方法
        3.detail参数用于指定该action要处理的是是否是详情资源对象(url是否需要传递pk值)
        :return:
        '''
        # 1.使用get_queryset()获取查询集的所有数据
        queryset = self.get_queryset()
        # 2.使用filter_queryset()方法过滤查询
        queryset = self.filter_queryset(queryset)
        # 3.使用paginate_queryset对排序和过滤后的数据进行分页，然后返回分页之后的查询集
        page = self.paginate_queryset(queryset)
        if page is not None:
            '''
            如果设置了分页引擎(也就是page不为None),则使用下边的代码对分页后的数据进行处理并返回给前端
            此处不能使用self.get_serializer(),如果使用它获取到的是ProjectModelSerializer序列化器，而不是ProjectNameModelSerializer序列化器
            因为返回的是多条数据，所以这里需要使用many=True
            '''
            serializer = ProjectNameModelSerializer(instance=page, many=True)
            # 4.返回分页后的数据给前端
            return self.get_paginated_response(serializer.data)
        '''如果返回给前端的是数组(多条数据)时，需要添加many=True关键字参数'''
        # 5.如果没有设置分页引擎(也就是page为None),则直接将排序或过滤后的数据进行处理并返回给前端
        serializer = ProjectNameModelSerializer(instance=queryset, many=True)
        '''将从数据库中获取到的数据返回给前端'''
        return Response(serializer.data)

