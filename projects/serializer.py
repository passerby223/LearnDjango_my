#!/usr/bin/python3
# @FileName    :serializer.py
# @Time        :2020/7/31 下午9:26
# @Author      :passerby223
# @Description :序列化类

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from projects.models import Projects

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
    name = serializers.CharField(label='项目名称', max_length=150, help_text='项目名称',
                                 validators=[UniqueValidator(queryset=Projects.objects.all(), message='项目名不能重复!'),
                                             is_unique_project_name])
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
