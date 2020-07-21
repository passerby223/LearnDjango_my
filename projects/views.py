from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
# 创建视图
def index(request):
    return HttpResponse("<h1>Index Page!</h1>")

# 创建视图
def hello(request):
    return HttpResponse("<h1>Hello Django!</h1>")
