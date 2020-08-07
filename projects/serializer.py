#!/usr/bin/python3
# @FileName    :serializer.py
# @Time        :2020/7/31 下午9:26
# @Author      :passerby223
# @Description :序列化类

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from projects.models import Projects
from interfaces.models import Interfaces

'''外部自定义校验器'''


# 创建自定义校验器
# 第一个参数为字段的值 eg：name
def is_unique_project_name(name):
    if '项目' not in name:
        raise serializers.ValidationError(detail='项目名称中必须包含`项目`字段')


# 1.继承Serializer类或者子类
class ProjectSerializer(serializers.Serializer):
    '''
    创建项目序列化器类
    '''
    '''
    1.序列化器中定义的类属性字段往往与模型类字段一一对应；也可以不对应，不对应时主要是用来对字段做检验
    2.label选项相当于verbose_name(接口文档中展示的内容)，help_text
    3.如果想让响应体内容只返回部分字段的话，就需要在当前序列化类中注释掉不需要返回的类属性
    4.read_only=True指定该字段只能进行序列化输出,不进行反序列化输入
    5.write_only=True指定该字段只能进行反序列化输入,不进行序列化输出
    6.如果不指定read_only=True的字段，默认即可以进行序列化输出，也可以进行反序列化输入
    '''
    id = serializers.IntegerField(label='ID', read_only=True)
    # validators为一个list，用于声明校验器
    # UniqueValidatorDRF自带的内置校验器，校验字段值是否唯一
    name = serializers.CharField(label='项目名称',
                                 max_length=150,
                                 min_length=10,
                                 help_text='项目名称',
                                 validators=[UniqueValidator(queryset=Projects.objects.all(),
                                                             message='项目名不能重复!'),
                                             is_unique_project_name],
                                 error_messages={'max_length': '项目名称长度不能超过150个字符!',
                                                 'min_length': '项目名称长度不能少于10个字符!'
                                                 })  # error_messages用于自定义校验失败提示的错误信息!
    leader = serializers.CharField(label='负责人', max_length=50, help_text='负责人')
    tester = serializers.CharField(label='测试人员', max_length=50, help_text='测试人员')
    developer = serializers.CharField(label='开发人员', max_length=50, help_text='开发人员')
    # allow_null相当于模型类中的null,allow_blank相当于模型类中的blank
    desc = serializers.CharField(label='项目描述', help_text='项目描述', allow_blank=True, default='', allow_null=True)

    '''
    字段校验器执行的顺序
    字段定义时的限制(包含validators列表中的条目从左往右进行校验) ——> 单字段的校验(validate_字段名的实例方法) ——> 多字段联合校验器(validate)
    '''
    '''内部自定义校验器'''

    # 单字段级别的校验，函数名称必须以`validate_`开头，以`字段名结尾`，比如：`validate_name`且不需要再name字段的validators校验器中声明
    def validate_name(self, value):
        if not value.endswith('项目'):
            raise serializers.ValidationError(detail='项目名称必须以`项目`结尾')
        # 如果校验通过，必须将字段值返回
        return value

    def validate(self, attrs):
        '''
        多字段联合校验器,方法名固定，参数固定
        :param attrs:
        :return:
        '''
        if 'Jack' not in attrs.get('tester') and 'Jack' not in attrs.get('leader'):
            raise serializers.ValidationError('Jack必须是项目负责人或者是项目测试人!')
        return attrs

    def create(self, validated_data):
        return Projects.objects.create(**validated_data)

    def update(self, instance, validated_data):
        '''校验成功后的数据，可以使用`序列化对象.validated_data`属性来获取校验成功后的数据'''
        instance.name = validated_data.get('name')
        instance.leader = validated_data.get('leader')
        instance.tester = validated_data.get('tester')
        instance.developer = validated_data.get('developer')
        instance.desc = validated_data.get('desc')
        instance.save()
        return instance


# 使用DRF自带的模型类序列化器
class ProjectModelSerializer(serializers.ModelSerializer):
    # validators为一个list，用于声明校验器
    # UniqueValidatorDRF自带的内置校验器，校验字段值是否唯一
    '''
    使用DRF自带的模型类序列化器时，如果需要`自定义校验器`的话，可以针对需要使用自定义校验器的字段单独进行设定校验器。
    它会覆盖掉DRF自动生成的该字段校验器
    '''

    # name = serializers.CharField(label='项目名称', max_length=150, help_text='项目名称',
    #                              validators=[UniqueValidator(queryset=Projects.objects.all(), message='项目名不能重复!'),
    #                                          is_unique_project_name])

    class Meta:
        # 1. 指定参考哪个模型类来创建模型类序列化器
        model = Projects
        # 2. 指定为模型类的哪些字段(__all__指定模型类中的所有字段)，来生成序列化器
        '''默认DRF会自动创建模型类的ID字段的read_only=True属性'''
        '''
        ①如果需要模型类的所有字段来生成模型类序列化器，则指定fields='__all__'，此时fields的值只能是`字符串`类型
        ②如果需要模型类的部分字段来生成模型类序列化器，则指定fields=(字段1, 字段2, ...)，此时fields的值只能是`元组`类型
        ③如果需要`除了模型类的部分字段外的其它字段`来生成模型类序列化器，则指定exclude=(字段1, 字段2, ...)，此时exclude的值只能是`元组`类型
        ④如果需要模型类的部分字段设置`read_only=True`属性，则指定read_only_fields=(字段1, 字段2, ...)，此时read_only_fields的值只能是`元组`类型
        '''
        fields = '__all__'
        # fields = ('id', 'name', 'leader', 'tester', 'developer')
        # exclude = ('developer', 'desc')
        # read_only_fields = ('leader', 'tester')
        # 使用extra_kwargs为字段添加其他属性:write_only属性需要通过这种方式来添加
        extra_kwargs = {
            'name': {
                # 'write_only': True,
                'min_length': 3,
                'error_messages': {'max_length': '项目名称长度不能超过150个字符!',
                                   'min_length': '项目名称长度不能少于3个字符!'},
                'validators': [UniqueValidator(queryset=Projects.objects.all(), message='项目名不能重复!'),
                               is_unique_project_name]
            },
            'leader': {
                # 'write_only': True,
                'min_length': 3,
                'error_messages': {'max_length': '负责人长度不能超过50个字符!',
                                   'min_length': '负责人长度不能少于3个字符!'}
            },
            'tester': {
                # 'write_only': True,
                'min_length': 3,
                'error_messages': {'max_length': '测试人员长度不能超过50个字符!',
                                   'min_length': '测试人员长度不能少于3个字符!'}
            },
            'developer': {
                # 'write_only': True,
                'min_length': 3,
                'error_messages': {'max_length': '开发人员长度不能超过50个字符!',
                                   'min_length': '开发人员长度不能少于3个字符!'}
            },

        }

    '''
    字段校验器执行的顺序
    字段定义时的限制(包含validators列表中的条目从左往右进行校验) ——> 单字段的校验(validate_字段名的实例方法) ——> 多字段联合校验器(validate)
    '''
    '''内部自定义校验器'''

    # 单字段级别的校验，函数名称必须以`validate_`开头，以`字段名结尾`，比如：`validate_name`且不需要在name字段的validators校验器中声明
    def validate_name(self, value):
        if not value.endswith('项目'):
            raise serializers.ValidationError(detail='项目名称必须以`项目`结尾')
        # 如果校验通过，必须将字段值返回
        return value

    def validate(self, attrs):
        '''
        多字段联合校验器,方法名固定，参数固定
        :param attrs:
        :return:
        '''
        if 'Jack' not in attrs.get('tester') and 'Jack' not in attrs.get('leader'):
            raise serializers.ValidationError('Jack必须是项目负责人或者是项目测试人!')
        return attrs

    '''DRF(需要继承serializers.ModelSerializer类)自动创建的字段校验器，会自动创建create()和update()方法，所以下边的代码(create和update方法)是多余的'''
    # def create(self, validated_data):
    #     return Projects.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     '''校验成功后的数据，可以使用`序列化对象.validated_data`属性来获取校验成功后的数据'''
    #     instance.name = validated_data.get('name')
    #     instance.leader = validated_data.get('leader')
    #     instance.tester = validated_data.get('tester')
    #     instance.developer = validated_data.get('developer')
    #     instance.desc = validated_data.get('desc')
    #     instance.save()
    #     return instance

class ProjectNameModelSerializer(serializers.ModelSerializer):
    '''
    获取所有项目的name序列化器
    '''
    class Meta:
        model = Projects
        # ②如果需要模型类的部分字段来生成模型类序列化器，则指定fields=(字段1, 字段2, ...)，此时fields的值只能是`元组`类型
        fields = ('id', 'name')


class InterfaceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interfaces
        fields = '__all__'


class InterfacesByProjectIdSerializer(serializers.ModelSerializer):
    interfaces_set = InterfaceDetailSerializer(read_only=True, many=True)

    class Meta:
        model = Projects
        fields = ('id', 'interfaces_set')