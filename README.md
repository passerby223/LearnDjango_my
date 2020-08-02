# 改变数据库模型步骤
1. 编辑当前app根目录下的`models.py`文件，改变模型
2. 为`app`模型的改变生成迁移文件
    ```bash
    python3 manage.py makemigrations 应用名称
    ```
3. 应用数据库迁移
    ```bash
    python3 manage.py migrate 应用名称
    ```
# 创建项目和应用步骤
1. 创建项目
    ```bash
    django-admin startproject 项目名称
    ```
2. 在`manage.py`文件所在目录下创建应用
    ```bash
    python3 manage.py startapp 应用名称
    ```
3. 去项目目录下的`settings.py`中注册子应用
    ```python
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # 注册子应用projects
        'projects.apps.ProjectsConfig'
    ]
    ```
# 创建项目`admin`后台的超级管理员,并访问`admin`后台页面
1. 迁移项目所有数据表
    ```bash
    python3 manage.py migrate
    ```
2. 创建超级管理员
    ```bash
    python3 manage.py createsuperuser
    # 根据终端提示进行操作即可
    ```
3. 去`app应用`目录下的`admin.py`中注册`app应用`对应的`models`
    ```python
    from django.contrib import admin
    from projects.models import Projects
    
    # Register your models here.
    
    admin.site.register(Projects)
    ```
4. 启动项目，打开`admin`后台管理页面`http://IP:端口号/admin/`，`账号密码`就是刚创建的`超级用户`的`账号及密码`
# 通过`python shell`练习`Django`中`ORM`的`CRUD`操作
1. 安装`ipython`
    ```bash
    pip3 install -i https://pypi.douban.com/simple ipython
    ```
2. 通过`python shell`激活一个`ipython`类型的终端，在该终端下操作会有智能提示
    ```bash
    python3 manage.py shell -i ipython
    ```
# 安装并配置DRF框架
1. 安装`DRF`
    ```bash
    pip3 install -i https://pypi.douban.com/simple djangorestframework
    # markdown为了接口在web中展示更好看
    pip3 install -i https://pypi.douban.com/simple markdown
    ```
2. 在`setting.py`文件中注册`DRF`
    ```bash
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # 注册子应用projects
        'projects.apps.ProjectsConfig',
        # 注册djangorestframework
        'rest_framework',
        'interfaces.apps.InterfacesConfig'
    ]
    ```
# DRF中使用开源的django-filter过滤引擎
```bash
# 安装
pip3 install -i https://pypi.douban.com/simple django-filter
# 配置
from django_filters.rest_framework import DjangoFilterBackend
# 视图类中指定Django-filter过滤引擎
filter_backends = [DjangoFilterBackend]
# 指定需要过滤的字段
filterset_fields = ['id', 'name', 'leader']
###############################################
# 在setting.py文件中中全局指定过滤引擎
# 注册app
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 注册子应用projects
    'projects.apps.ProjectsConfig',
    # 注册djangorestframework
    'rest_framework',
    # 注册django-filter
    'django_filters',
    'interfaces.apps.InterfacesConfig',
]
# 指定全局过滤器
REST_FRAMEWORK = {
    # 默认响应渲染类
    'DEFAULT_RENDERER_CLASSES': (
        # json渲染器为第一优先级
        'rest_framework.renderers.JSONRenderer',
        # 可浏览的浏览器中html格式的API渲染器为第二优先级
        # 'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    # 全局指定过滤引擎,对所有类视图有效。也可以在类视图中单独指定过滤引擎，只对当前类视图有效
    # 全局指定排序过滤引擎
    # 'DEFAULT_FILTER_BACKENDS': ['rest_framework.filters.OrderingFilter'],
    # 全局指定django-filter过滤引擎
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}
```