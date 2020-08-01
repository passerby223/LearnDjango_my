import json
from django.http import HttpResponse, JsonResponse, Http404
from django.views import View
from projects.serializer import ProjectModelSerializer, ProjectModelSerializer
from projects.models import Projects


class ProjectsList(View):
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
        '''2.将数据库模型类实例转化为dict类型(嵌套dict的list)'''
        # project_list = []
        # for project in result:
        #     project_list.append({
        #         "name": project.name,
        #         "leader": project.leader,
        #         "tester": project.tester,
        #         "developer": project.developer,
        #         "desc": project.desc
        #     })
        '''如果返回给前端的是数组(多条数据)时，需要添加many=True关键字参数'''
        serializer_data = ProjectModelSerializer(instance=obj_pro, many=True)
        # JsonResponse第一个参数默认只能为dict字典，如果要设置为其他数据类型，需要设置safe=False
        '''3. 将从数据库中获取到的数据返回给前端'''
        return JsonResponse(serializer_data.data, safe=False)

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
            return JsonResponse(serializer_data.errors)
        '''3.向数据库中添加一条数据，新增项目'''
        '''校验成功后的数据，可以使用`序列化对象.validated_data`属性来获取校验成功后的数据'''
        '''
        在创建序列化器时，如果给data传参，那么在调用`序列化器.save()`方法时，会自动化调用序列化器对象的create()方法
        '''
        serializer_data.save()
        '''4.将序列化数据返回给前端'''
        return JsonResponse(serializer_data.data, status=201)


class ProjectsDetail(View):

    # 将获取指定ID为pk值的项目单独抽离出来为一个方法
    def get_project(self, pk):
        try:
            return Projects.objects.get(id=pk)
        except Projects.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        '''1.校验前端传递的pk(项目ID)值，类型是否正确(正整数),在数据库中是否存在'''
        '''2.获取指定ID为pk值的项目'''
        obj_pro = self.get_project(pk=pk)
        # 3.将模型类对象转化为字典，返回给前端
        '''序列化'''
        # res_data = {
        #     "id": obj_pro.id,
        #     "name": obj_pro.name,
        #     "leader": obj_pro.leader,
        #     "tester": obj_pro.tester,
        #     "developer": obj_pro.developer,
        #     "desc": obj_pro.desc
        # }
        '''通过模型类对象(或者查询集)，传给instance可进行序列化操作'''
        '''通过序列化器ProjectModelSerializer对象的data属性，就可以获取序列化后的字典'''
        serializer_data = ProjectModelSerializer(instance=obj_pro)
        return JsonResponse(serializer_data.data)

    def put(self, request, pk):
        '''1.校验前端传递的pk(项目ID)值，类型是否正确(正整数),在数据库中是否存在'''
        '''2.获取指定ID为pk值的项目'''
        obj_pro = self.get_project(pk=pk)
        # 从前端获取json数据并转化为Python中的dict类型数据
        # 为了严禁性，这里需要做各种复杂的校验
        # 比如：是否为json、传递的项目数据是否符合要求、有些比传参数是否携带等
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
            return JsonResponse(serializer_data.errors)
        '''4.更新项目, 通过前端传递过来的数据对字段值进行修改'''
        serializer_data.save()
        '''5.序列化数据，返回给前端'''
        return JsonResponse(serializer_data.data, status=201)

    def delete(self, request, pk):
        '''1.校验前端传递的pk(项目ID)值，类型是否正确(正整数),在数据库中是否存在'''
        '''2.获取指定ID为pk值的项目'''
        obj_pro = self.get_project(pk=pk)
        obj_pro.delete()
        return JsonResponse(None, safe=False, status=204)
