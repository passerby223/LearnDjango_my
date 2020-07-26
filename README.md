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
    ```bash
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