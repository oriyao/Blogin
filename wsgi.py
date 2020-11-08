"""
# coding:utf-8
@Time    : 2020/11/07
@Author  : oriyao
@mail    : ylzhangyao@gmail.com
@File    : wsgi
@Describe: Flask 入口文件
"""
from blogin import create_app

app = create_app('production')
