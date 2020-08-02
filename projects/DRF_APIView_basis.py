#!/usr/bin/python3
# @FileName    :DRF_APIView_basis.py
# @Time        :2020/8/2 下午4:19
# @Author      :passerby223
# @Description :
import json
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from projects.serializer import ProjectModelSerializer
from projects.models import Projects


class ProjectsList(APIView):
    '''
    创建接口的步骤
    1.校验用户数据
    2.数据反序列化
    3.操作数据库
    4.数据序列化
    '''

    def get(self, request):
        '''
        获取所有项目
        :param request:
        :return:
        '''
        '''1.从数据库获取所有项目信息'''
        obj_pro = Projects.objects.all()
        '''如果返回给前端的是数组(多条数据)时，需要添加many=True关键字参数'''
        serializer_data = ProjectModelSerializer(instance=obj_pro, many=True)
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
        serializer_data = ProjectModelSerializer(data=dict_data)
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


class ProjectsDetail(APIView):

    # 将获取指定ID为pk值的项目单独抽离出来为一个方法
    def get_object(self, pk):
        try:
            return Projects.objects.get(id=pk)
        except Projects.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        '''1.校验前端传递的pk(项目ID)值，类型是否正确(正整数),在数据库中是否存在'''
        '''2.获取指定ID为pk值的项目'''
        obj_pro = self.get_object(pk=pk)
        # 3.将返回的数据序列化成json格式数据，返回给前端
        serializer_data = ProjectModelSerializer(instance=obj_pro)
        # 如果前端请求中未指定Accept，那么默认返回json格式数据
        return Response(serializer_data.data, status=200)

    def put(self, request, pk):
        '''1.校验前端传递的pk(项目ID)值，类型是否正确(正整数),在数据库中是否存在'''
        '''2.获取指定ID为pk值的项目'''
        obj_pro = self.get_object(pk=pk)
        json_data = request.body.decode('utf-8')
        dict_data = json.loads(json_data, encoding='utf-8')
        '''3.校验前端输入的数据'''
        '''反序列化使用data参数'''
        '''
        在创建序列化器时，如果同时给instance和data传参，那么在调用`序列化器.save()`方法时，会自动化调用序列化器对象的update()方法
        '''
        serializer_data = ProjectModelSerializer(instance=obj_pro, data=dict_data)
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
        obj_pro = self.get_object(pk=pk)
        obj_pro.delete()
        return Response(None, status=204)
