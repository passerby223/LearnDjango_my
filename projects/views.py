import json
from django.http import HttpResponse, JsonResponse
from django.views import View
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
        # 1.从数据库获取所有项目信息
        result = Projects.objects.all()
        # 2.将数据库模型类实例转化为dict类型(嵌套dict的list)
        project_list = []
        for project in result:
            project_list.append({
                "name": project.name,
                "leader": project.leader,
                "tester": project.tester,
                "developer": project.developer,
                "desc": project.desc
            })
        # JsonResponse第一个参数默认只能为dict字典，如果要设置为其他数据类型，需要设置safe=False
        return JsonResponse(project_list, safe=False)

    def post(self, request):
        '''
        新建项目
        :param request:
        :return:
        '''
        # 1.从前端获取json数据并转化为Python中的dict类型数据
        # 为了严禁性，这里需要做各种复杂的校验
        # 比如：是否为json、传递的项目数据是否符合要求、有些比传参数是否携带等
        # 反序列化数据
        json_data = request.body.decode('utf-8')
        dict_data = json.loads(json_data, encoding='utf-8')
        # 2.向数据库中添加一条数据，新增项目
        # obj_pro = Projects.objects.create(
        #     name=dict_data.get('name'),
        #     leader=dict_data.get('leader'),
        #     tester=dict_data.get('tester'),
        #     developer=dict_data.get('developer'),
        #     desc=dict_data.get('desc')
        # )
        obj_pro = Projects.objects.create(**dict_data)
        # 3.将模型类对象转化为字典，然后返回
        # 序列化数据
        res_data = {
            "id": obj_pro.id,
            "name": obj_pro.name,
            "leader": obj_pro.leader,
            "tester": obj_pro.tester,
            "developer": obj_pro.developer,
            "desc": obj_pro.desc
        }
        return JsonResponse(res_data, status=201)

class ProjectsDetail(View):

    def get(self, request, pk):
        # 1.校验前端传递的pk(项目ID)值，类型是否正确(正整数),在数据库中是否存在
        # 2.获取指定ID为pk值的项目
        obj_pro = Projects.objects.get(id=pk)
        # 3.将模型类对象转化为字典，返回给前端
        res_data = {
            "id": obj_pro.id,
            "name": obj_pro.name,
            "leader": obj_pro.leader,
            "tester": obj_pro.tester,
            "developer": obj_pro.developer,
            "desc": obj_pro.desc
        }
        return JsonResponse(res_data)

    def put(self, request, pk):
        # 1.校验前端传递的pk(项目ID)值，类型是否正确(正整数),在数据库中是否存在
        # 2.获取指定ID为pk值的项目
        obj_pro = Projects.objects.get(id=pk)
        # 3.从前端获取json数据并转化为Python中的dict类型数据
        # 为了严禁性，这里需要做各种复杂的校验
        # 比如：是否为json、传递的项目数据是否符合要求、有些比传参数是否携带等
        json_data = request.body.decode('utf-8')
        dict_data = json.loads(json_data, encoding='utf-8')
        # 4.通过前端传递过来的数据对字段值进行修改
        obj_pro.name = dict_data.get('name')
        obj_pro.leader = dict_data.get('leader')
        obj_pro.tester = dict_data.get('tester')
        obj_pro.developer = dict_data.get('developer')
        obj_pro.desc = dict_data.get('desc')
        # 保存更新
        obj_pro.save()
        # 5.将模型类对象转化为字典，返回给前端
        res_data = {
            "id": obj_pro.id,
            "name": obj_pro.name,
            "leader": obj_pro.leader,
            "tester": obj_pro.tester,
            "developer": obj_pro.developer,
            "desc": obj_pro.desc
        }
        return JsonResponse(res_data, status=201)
    def delete(self, request, pk):
        # 1.校验前端传递的pk(项目ID)值，类型是否正确(正整数),在数据库中是否存在
        # 2.获取指定ID为pk值的项目
        obj_pro = Projects.objects.get(id=pk)
        obj_pro.delete()
        return JsonResponse(None, safe=False, status=204)