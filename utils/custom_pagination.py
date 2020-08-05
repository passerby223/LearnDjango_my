#!/usr/bin/python3
# @FileName    :custom_pagination.py
# @Time        :2020/8/4 上午12:31
# @Author      :passerby223
# @Description :自定义查询数据结果分页展示效果类
from rest_framework.pagination import PageNumberPagination


class PageNumberPaginationCustom(PageNumberPagination):
    '''
    自定义查询数据结果分页展示效果类
    ①全局配置(对所有类视图有效)：
    需要去setting.py文件中设置默认分页引擎为当前的py文件
    ②也可以在单个类视图中单独指定，只对当前视图有效
    '''
    # 指定前端调分页接口时`分页参数`为p(默认是page)，比如：http -v :8000/api/v1/projects/ p==2
    page_query_param = 'p'
    # 默认情况下，每一页显示的数据条数为2,可以在前端通过入参`s`参数任意指定条数为其他数值
    # 比如：http -v :8000/api/v1/projects/ p==1 s==4
    page_size = 5
    # 指定前端调分页接口时`分页大小参数`为s(默认为空)，比如：http -v :8000/api/v1/projects/ p==2 s==4
    page_size_query_param = 's'
    # 指定前端能分页的最大页数为50
    max_page_size = 50