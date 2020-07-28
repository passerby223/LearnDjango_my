from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from projects.models import Projects

# Create your views here.
'''
函数视图
如果函数视图中逻辑处理代码过多时，会导致代码混乱且不容易维护，所以引入类视图
'''
# 创建视图
def index(request):
    '''
    视图函数
    :param request: HttpRequest对象，包含前端用户的所有请求信息
    :return:必须返回一个HttpResponse对象或子对象
    '''
    return HttpResponse("<h1>Index Page!</h1>")


# 创建视图
def hello(request):
    return HttpResponse("<h1>Hello Django!</h1>")


'''
类视图
'''
class ProjectsView(View):
    # def get(self, request, pk=None):
    #     '''
    #     # 1.使用request.GET来获取查询字符串参数
    #     # 2.request.GET返回的是一个类字典对象，支持字典中的所有操作。
    #     # 3.获取到的查询字符串参数中，如果有多个参数key值相同，
    #       则使用request.GET.get('key值')获取到的value值是查询字符串路径中最后一个key的value值。
    #       可以使用request.GET.getlist('key值')来获取多个相同key值的参数。
    #     # 4.使用projectId来获取路径参数中的变量
    #     :param request:HttpRequest对象，包含前端用户的所有请求信息
    #     :param projectId:接收路径参数中的变量
    #     :return:
    #     '''
    #     if pk:
    #         data = {
    #             'name': 'tester',
    #             'projectId': pk
    #         }
    #         # return HttpResponse(f"<h1>GET>>>Project {pk} Detail Page!</h1>")
    #         # 传入字典，返回json格式数据
    #         return JsonResponse(data)
    #     else:
    #         return HttpResponse("<h1>GET>>>Projects Page!</h1>")
    def get(self, request, pk=None):
        '''
        :param request:HttpRequest对象，包含前端用户的所有请求信息
        :param projectId:接收路径参数中的变量
        '''
        '''
        新增数据(Create)
        '''
        '''
        新增数据方法一
        '''
        # 创建模型类对象，此时并未执行SQL语句
        # obj01 = Projects(name='销售品管理平台', leader='Mike', tester='tester03', developer='developer03', desc='销售品管理平台接口自动化')
        # 调用save()方法保存后，才回去数据库中执行插入数据的SQL
        # obj01.save()
        '''
        新增数据方法二
        '''
        # Projects.objects.create(name='天翼优惠券平台', leader='Lucy', tester='tester04', developer='developer04', desc='天翼优惠券平台接口自动化项目')
        '''
        查询数据(Retrieve)
        '''
        '''
        1. 查询表内所有数据
        '''
        # 获取table所有数据,返回一个QuerySet查询集(列表)，
        result1 = Projects.objects.all()
        first_data_name_field_value = result1[0].name # 订单管理平台
        '''
        2. 获取某一条指定的数据使用get()方法
            ①get()方法只能返回一条数据
            ②如果返回多条数据或者查询的数据不存在就会抛出异常
            ③get()方法的参数往往为`主键`或者`唯一键`
        '''
        result2 = Projects.objects.get(id=1) # result2=订单管理平台
        result3 = Projects.objects.get(id=2) # result3=新生产平台
        '''
        3. 获取多条数据，使用filter()或者exclude()方法
            使用filter返回的是满足条件的QuerySet，exclude()方法返回的是不满足条件的QuerySet
        '''
        result4 = Projects.objects.filter(leader='Jack') # result4=QuerySet
        result5 = Projects.objects.exclude(leader='Jack') # result5=QuerySet
        '''
        4. 使用filter()过滤方法的特定用法
            ①filter(模型类属性名(字段名)__contains)将包含指定字符串的所有数据返回
            ②filter(模型类属性名(字段名)__icontains)忽略大小写
            ③将startwith以给定字符串开头的所有数据返回
            ④将in以给定范围的字符串的所有数据返回
        '''
        result6 = Projects.objects.filter(leader__contains='Jack')
        result7 = Projects.objects.filter(leader__icontains='Jack')
        result8 = Projects.objects.filter(leader__startswith='Ja')
        result9 = Projects.objects.filter(leader__endswith='ck')
        result10 = Projects.objects.filter(leader__in=['Lucy', 'Jack', 'Tom', 'jack'])
        '''
        5. 通过外键进行关联查询
            filter(外键字段__从表字段名__contains)
        '''
        # 获取新建销售品接口所在的项目
        result11 = Projects.objects.filter(interfaces__name='新建销售品') # 销售品管理平台
        pass
        return JsonResponse({"hello": "world"})

    def post(self, request):
        '''
        # 1. 使用request.POST.get('key值')来获取www-form表单参数
        # 2. 使用request.body来获取编码后的字节bytes类型的json格式请求体参数
        # 3. 使用request.FILES来获取文件类型的请求体参数
        :param request:HttpRequest对象，包含前端用户的所有请求信息
        :return:
        '''
        return HttpResponse("<h1>POST>>>Projects Page!</h1>")
    def put(self, request):
        return HttpResponse("<h1>PUT>>>Projects Page!</h1>")
    def delete(self, request):
        return HttpResponse("<h1>DELETE>>>Projects Page!</h1>")
