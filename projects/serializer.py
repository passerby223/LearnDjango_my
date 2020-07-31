#!/usr/bin/python3
# @FileName    :serializer.py
# @Time        :2020/7/31 下午9:26
# @Author      :passerby223
# @Description :序列化类

from rest_framework import serializers


# 1.继承Serializer类或者子类
class ProjectSerializer(serializers.Serializer):
    '''
    创建项目序列化器类
    '''
    # label选项相当于verbose_name(接口文档中展示的内容)，help_text
    # 如果想让响应体内容只返回部分字段的话，就需要在当前序列化类中注释掉不需要返回的类属性
    '''
    read_only=True指定该字段只能进行序列化输出,不进行反序列化输入
    write_only=True指定该字段只能进行反序列化输入,不进行序列化输出
    如果不指定read_only=True的字段，默认即可以进行序列化输出，也可以进行反序列化输入
    '''
    id = serializers.IntegerField(label='ID', read_only=True)
    name = serializers.CharField(label='项目名称', max_length=150, help_text='项目名称')
    leader = serializers.CharField(label='负责人', max_length=50, help_text='负责人')
    tester = serializers.CharField(label='测试人员', max_length=50, help_text='测试人员')
    developer = serializers.CharField(label='开发人员', max_length=50, help_text='开发人员')
    # allow_null相当于模型类中的null,allow_blank相当于模型类中的blank
    desc = serializers.CharField(label='项目描述', help_text='项目描述', allow_blank=True, default='', allow_null=True)

