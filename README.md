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