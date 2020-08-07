"""LearnDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# from rest_framework import permissions
# from projects.views import index

# 第二种自动生成接口文档的方法，并且需要在urlpatterns列表中定义接口文档的路由
schema_view = get_schema_view(
    openapi.Info(
        # 必传
        title="测试平台接口文档",
        # 必传
        default_version='v1',
        description="测试平台项目接口文档",
        terms_of_service="www.wenbin.org.cn",
        contact=openapi.Contact(email="1912315910@qq.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    # 权限类
    # permission_classes=(permissions.AllowAny,),
)


# 全局路由表
# 1. urlpatterns为固定名称的列表
# 2. 列表中一个元素就代表一条路由信息
# 3. 从上往下匹配，如果能匹配上,会直接调用path里边的视图方法，如index
# 4. 如果匹配不上，会自动抛出一个404异常
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('index/', index),
    # 这里使用include代表，当在前端访问`http://127.0.0.1:8000/hello/`时，
    # 会从子应用projects的路由表urls文件中去查找对应的路由，执行对应路由绑定的视图方法
    # path('hello/', include('projects.urls')),
    # 类视图的父路由
    path('api/v1/', include('projects.urls')),
    path('docs/', include_docs_urls(title='测试平台接口文档', description='测试平台接口文档')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
