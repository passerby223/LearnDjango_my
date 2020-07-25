from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View

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
    def get(self, request, pk=None):
        '''
        # 1.使用request.GET来获取查询字符串参数
        # 2.request.GET返回的是一个类字典对象，支持字典中的所有操作。
        # 3.获取到的查询字符串参数中，如果有多个参数key值相同，
          则使用request.GET.get('key值')获取到的value值是查询字符串路径中最后一个key的value值。
          可以使用request.GET.getlist('key值')来获取多个相同key值的参数。
        # 4.使用projectId来获取路径参数中的变量
        :param request:HttpRequest对象，包含前端用户的所有请求信息
        :param projectId:接收路径参数中的变量
        :return:
        '''
        if pk:
            data = {
                'name': 'tester',
                'projectId': pk
            }
            # return HttpResponse(f"<h1>GET>>>Project {pk} Detail Page!</h1>")
            # 传入字典，返回json格式数据
            return JsonResponse(data)
        else:
            return HttpResponse("<h1>GET>>>Projects Page!</h1>")
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
