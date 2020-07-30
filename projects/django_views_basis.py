#!/usr/bin/python3
# @FileName    :django_views_basis.py
# @Time        :2020/7/30 下午10:05
# @Author      :passerby223
# @Description :django视图和ORM相关基础知识

from django.http import HttpResponse, JsonResponse
from django.views import View
from projects.models import Projects
from django.db.models import Q

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
        result4_ = Projects.objects.filter(leader='Mike') # result4=QuerySet
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
        '''
        6. 比较查询
            __gt：>
            __gte：>=
            __lt：<
            __lte：<=
        '''
        result12 = Projects.objects.filter(id=2)
        result13 = Projects.objects.filter(id__gt=2)
        result14 = Projects.objects.filter(id__gte=2)
        result15 = Projects.objects.filter(id__lt=2)
        result16 = Projects.objects.filter(id__lte=2)
        '''
        7. 逻辑关系，多个条件查询
            ①如果给filter指定多个条件，那么条件之间是与的关系
            ②可以使用Q变量指定多个条件，那么条件之间是或的关系
        '''
        result17 = Projects.objects.filter(leader='Jack', name__contains='管理')
        result18 = Projects.objects.filter(Q(leader='Mike') | Q(tester='tester01'))
        '''
        8. 查询集(QuerySet)操作
            ①查询集相当于一个列表，支持列表中的大多数操作
                通过数字索引获取值，
                支持正向切片，不支持反向切片(负数)
                for循环
            ②查询集是对数据库操作的一种优化
                查询集会缓存查询结果
            ③支持惰性查询
            ④支持链式操作
                first()返回查询集中的第一条数据
                last()返回查询集中的最后一条数据
                
        '''
        # first()返回查询集中的第一条数据
        result19 = Projects.objects.filter(leader__contains='ac').first()
        # last()返回查询集中的最后一条数据
        result20 = Projects.objects.filter(leader__contains='ac').last()
        # 支持链式操作
        result21 = Projects.objects.filter(leader__contains='ac').filter(developer='developer05')
        '''
        更新数据(update)
            a.先获取到要修改的模型对象
            b.进行修改操作
            c.保存修改
        '''
        # obj_pro_01 = Projects.objects.get(id=5)
        # obj_pro_01.desc = '合伙人平台接口自动化'
        # obj_pro_01.save()
        '''
        删除数据(delete)
            a.先获取到要删除的模型对象
            b.进行删除操作(删除操作默认会执行保存)
        '''
        # obj_pro_02 = Projects.objects.filter(leader='Jack').filter(name__contains='删除')
        # obj_pro_02.delete()
        '''
        排序操作
            使用order_by()方法进行排序，默认从小到大排序；在字段名前加一个`-`号，代表从大到小排序
            如果order_by()方法中第一个参数排序的结果都相同，则使用第二个参数进行排序
        '''
        # 从小到大排序
        result22 = Projects.objects.filter(id__gte=2).order_by('id', 'name')
        # 从大到小排序
        result23 = Projects.objects.filter(id__gte=2).order_by('-id', 'name')
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
