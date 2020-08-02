import json
from django.http import Http404
from rest_framework import filters
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend, filterset

from projects.serializer import ProjectModelSerializer
from projects.models import Projects

# 继承GenericAPIView基类，GenericAPIView基类可以提供过滤，排序，分页功能
class ProjectsList(GenericAPIView):
    '''
    创建接口的步骤
    1.校验用户数据
    2.数据反序列化
    3.操作数据库
    4.数据序列化
    '''
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
    def get(self, request):
        '''
        获取所有项目
        :param request:
        :return:
        '''
        '''1.从数据库获取所有项目信息'''
        # 5.使用get_queryset()获取查询集的所有数据
        obj_pro = self.get_queryset()
        # 6.使用filter_queryset()方法过滤查询
        obj_pro = self.filter_queryset(obj_pro)
        '''如果返回给前端的是数组(多条数据)时，需要添加many=True关键字参数'''
        serializer_data = self.get_serializer(instance=obj_pro, many=True)
        '''3. 将从数据库中获取到的数据返回给前端'''
        return Response(serializer_data.data)

    def post(self, request):
        '''
        新建项目
        :param request:
        :return:
        '''
        '''1.从前端获取json数据并转化为Python中的dict类型数据'''
        # 为了严禁性，这里需要做各种复杂的校验
        # 比如：是否为json、传递的项目数据是否符合要求、有些比传参数是否携带等
        '''反序列化数据'''
        json_data = request.body.decode('utf-8')
        dict_data = json.loads(json_data, encoding='utf-8')
        '''2.校验前端输入的数据'''
        # 反序列化使用data参数
        '''
        在创建序列化器时，如果给data传参，那么在调用`序列化器.save()`方法时，会自动化调用序列化器对象的create()方法
        '''
        serializer_data = self.get_serializer(data=dict_data)
        # 调用序列化器对象的is_valid()方法来校验前端传入的参数，如果校验成功返回True，否则返回失败
        # 如果raise_exception=True，那么校验失败后，会抛出异常
        try:
            serializer_data.is_valid(raise_exception=True)
        except Exception as e:
            # 当调用is_valid()方法后，才可以调用errors属性，获取校验失败返回的错误提示信息
            return Response(serializer_data.errors)
        '''3.向数据库中添加一条数据，新增项目'''
        '''校验成功后的数据，可以使用`序列化对象.validated_data`属性来获取校验成功后的数据'''
        '''
        在创建序列化器时，如果给data传参，那么在调用`序列化器.save()`方法时，会自动化调用序列化器对象的create()方法
        '''
        serializer_data.save()
        '''4.将序列化数据返回给前端'''
        return Response(serializer_data.data, status=201)

# 1. 需要继承GenericAPIView基类
class ProjectsDetail(GenericAPIView):
    # 2.必须指定queryset和serializer_class类属性
    # queryset用于指定需要使用的查询集
    queryset = Projects.objects.all()
    # serializer_class指定需要使用到的序列化器类
    serializer_class = ProjectModelSerializer
    '''
    使用lookup_field类属性，可以修改主键路由名称(就是api路径参数中的pk值，默认为pk，可以使用该属性进行覆盖。)
    如果修改了，路径参数也得同步更新
    '''
    # lookup_field = 'id'
    # 将获取指定ID为pk值的项目单独抽离出来为一个方法
    # def get_object(self, pk):
    #     try:
    #         return Projects.objects.get(id=pk)
    #     except Projects.DoesNotExist:
    #         raise Http404

    def get(self, request, pk):
        '''1.校验前端传递的pk(项目ID)值，类型是否正确(正整数),在数据库中是否存在'''
        '''2.获取指定ID为pk值的项目'''
        '''
        如果继承了GenericAPIView基类，则不需要在手动创建get_object()这个方法了。
        GenericAPIView类中默认会提供get_object()这个方法且不需要传参数(pk)
        '''
        obj_pro = self.get_object()
        # 3.将返回的数据序列化成json格式数据，返回给前端
        # 使用get_serializer()方法获取序列化器类
        serializer_data = self.get_serializer(instance=obj_pro)
        # 如果前端请求中未指定Accept，那么默认返回json格式数据
        return Response(serializer_data.data, status=200)

    def put(self, request, pk):
        '''1.校验前端传递的pk(项目ID)值，类型是否正确(正整数),在数据库中是否存在'''
        '''2.获取指定ID为pk值的项目'''
        obj_pro = self.get_object()
        json_data = request.body.decode('utf-8')
        dict_data = json.loads(json_data, encoding='utf-8')
        '''3.校验前端输入的数据'''
        '''反序列化使用data参数'''
        '''
        在创建序列化器时，如果同时给instance和data传参，那么在调用`序列化器.save()`方法时，会自动化调用序列化器对象的update()方法
        '''
        serializer_data = self.get_serializer(instance=obj_pro, data=dict_data)
        '''
        调用序列化器对象的is_valid()方法来校验前端传入的参数，如果校验成功返回True，否则返回失败
        如果raise_exception=True，那么校验失败后，会抛出异常
        '''
        try:
            serializer_data.is_valid(raise_exception=True)
        except Exception as e:
            # 当调用is_valid()方法后，才可以调用errors属性，获取校验失败返回的错误提示信息
            return Response(serializer_data.errors)
        '''4.更新项目, 通过前端传递过来的数据对字段值进行修改'''
        serializer_data.save()
        '''5.序列化数据，返回给前端'''
        return Response(serializer_data.data, status=201)

    def delete(self, request, pk):
        '''1.校验前端传递的pk(项目ID)值，类型是否正确(正整数),在数据库中是否存在'''
        '''2.获取指定ID为pk值的项目'''
        obj_pro = self.get_object()
        obj_pro.delete()
        return Response(None, status=204)
