from django.db import models


# Create your models here.
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
    name = models.CharField(verbose_name='接口名称', max_length=150, unique=True, help_text='接口名称')
    tester = models.CharField(verbose_name='测试人员', max_length=50, help_text='测试人员')
    # 11. null设置数据库中该字段是否为空；blank设置前端可以不传该字段，往往和null一起使用；default设置该字段默认值。
    desc = models.TextField(verbose_name='接口描述', help_text='接口描述', blank=True, default='', null=True)
    '''
    项目和接口属于一对多关系(一个项目中会有多个接口)，所以要创建这两个表的外键关系，需要在`多`的一侧(interfaces接口表)创建`一`(projects项目表)的外键。
    projects项目表为父表，interfaces接口表为字表。
    '''
    '''
    ForeignKey()方法中第1个参数(to)：
        1.如果两个模型类在不同的app下:
            ①填写格式可以为：`应用名字.模型类的类名` eg：models.ForeignKey('projects.Projects')
            ②也可以现在当前app下的`models.py`文件下导入另一个app下的模型类，然后直接填写`模型类类名`即可。eg：models.ForeignKey(User)
        2.如果两个模型类在相同的app下，填写格式为：模型类的类名。eg：models.ForeignKey(User)
    ForeignKey()方法中第2个参数(on_delete)：
        1.on_delete设置的是，当父表(projects项目表)删除之后，该外键字段(project)的处理方式(该怎么去处理)。
        2.可选参数
            ①models.CASCADE ===> 字表中该字段(project)也会被删除。
            ②models.SET_NULL ===> 字表中该字段(project)会被设置为None，需要先设置该字段null=True
            ③models.SET_DEFAULT ===> 字表中该字段(project)会被设置为一个默认值；同时需要指定默认值
            ④models.PROTECT ===> 会报错
            ①CASCADE
                级联删除
                删除包含ForeignKey的对象。
            ②PROTECT
                通过引发ProtectedError的子类django.db.IntegrityError来 防止删除引用的对象(抛出异常)
            ③SET_NULL
                将引用的对象设置为ForeignKey为null
            ④SET_DEFAULT 
                将ForeignKey其设置为默认值
                ForeignKey必须设置默认值
                例如上面的代码中:
                    author = models.ForeignKey(to='User', on_delete=models.SET_DEFAULT, related_name='user')
                    则在User表中必须设置默认值
            ⑤SET(表达式)
                将设置为ForeignKey传递给的值SET()或者如果传递了callable，则调用它的结果
            ⑥DO_NOTHING
                不采取行动
    '''
    project = models.ForeignKey('projects.Projects', on_delete=models.SET_DEFAULT(), verbose_name='所属项目', help_text='所属项目')

    # 定义子类Meta，用于设置当前数据库模型的元数据信息
    class Meta:
        # 修改表名
        db_table = 'tb_interfaces'
        # 设置在admin站点中的显示表名，在英文表名下表现为单数形式
        verbose_name = '接口'
        # 在英文表名下表现为复数形式，会自动在英文表名后边加一个`s`
        verbose_name_plural = '接口'
