from django.contrib import admin
from projects.models import Projects

class ProjectsAdmin(admin.ModelAdmin):
    '''
    定制后台admin管理站点类
    '''
    # 指定在修改(新增)中要显示的字段
    fields = ['name', 'leader', 'tester', 'developer', 'desc']
    # 指定projects列表页要列出的字段
    list_display = ['id', 'name', 'leader', 'tester', 'developer', 'desc']
# Register your models here.
# 注册`app应用`对应的`models`
admin.site.register(Projects, ProjectsAdmin)
