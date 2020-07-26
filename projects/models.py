from django.db import models

# Create your models here.
'''
1. 每一个应用下的数据库模型类，需要在当前应用下的models.py文件中进行定义
2. 一个数据库模型类相当于一个数据表(table)
3. 一个数据库模型类需要继承Model或者Model的子类
'''


class Projects(models.Model):
    '''
    创建projects模型类
    4. 定义一个类属性，相当于数据表中的一个字段
    5. 默认会创建一个自动递增的id主键
    6. 默认创建的数据库名称为：应用名小写_数据库模型类小写
    7. max_length为字段最大长度
    8. verbose_name为字段注释
    9. unique用于设置当前字段是否唯一，默认unique=False
    10. help_text用于在api文档中展示的名称
    '''
    name = models.CharField(verbose_name='项目名称', max_length=150, unique=True, help_text='项目名称')
    leader = models.CharField(verbose_name='负责人', max_length=50, help_text='负责人')
    tester = models.CharField(verbose_name='测试人员', max_length=50, help_text='测试人员')
    developer = models.CharField(verbose_name='开发人员', max_length=50, help_text='开发人员')
    # 11. null设置数据库中该字段是否为空；blank设置前端可以不传该字段，往往和null一起使用；default设置该字段默认值。
    desc = models.TextField(verbose_name='项目描述', help_text='项目描述', blank=True, default='', null=True)

    # 定义子类Meta，用于设置当前数据库模型的元数据信息
    class Meta:
        # 修改表名
        db_table = 'tb_projects'
        # 设置在admin站点中的显示表名，在英文表名下表现为单数形式
        verbose_name = '项目'
        # 在英文表名下表现为复数形式，会自动在英文表名后边加一个`s`
        verbose_name_plural = '项目'
