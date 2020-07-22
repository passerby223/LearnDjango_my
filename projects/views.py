from django.shortcuts import render
from django.http import HttpResponse
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
    def get(self, request):
        return HttpResponse("<h1>GET>>>Projects Page!</h1>")
    def post(self, request):
        return HttpResponse("<h1>POST>>>Projects Page!</h1>")
    def put(self, request):
        return HttpResponse("<h1>PUT>>>Projects Page!</h1>")
    def delete(self, request):
        return HttpResponse("<h1>DELETE>>>Projects Page!</h1>")
