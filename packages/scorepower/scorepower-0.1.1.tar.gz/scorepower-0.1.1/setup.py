'''
@Author: your name
@Date: 2020-06-28 20:45:17
@LastEditTime: 2020-08-07 16:41:52
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /scorePower/src/setup.py
''' 
# -*- coding: utf-8 -*-
# try:
#     from setuptools import setup
# except ImportError:
#     from distutils.core import setup
# import setuptools

# setup(
#     name='ss',  # 包的名字
#     author='bruce',  # 作者
#     version='0.1.0',  # 版本号
#     license='MIT',

#     description='project describe',  # 描述
#     long_description='''long description''',
#     author_email='xxx@163.com',  # 你的邮箱**
#     url='https://xxx',  # 可以写github上的地址，或者其他地址
#     # 包内需要引用的文件夹
#     packages=setuptools.find_packages(exclude=['url2io',]),
#     # packages=["src"],
#     # keywords='NLP,tokenizing,Chinese word segementation',
#     # package_dir={'jieba':'jieba'},
#     # package_data={'jieba':['*.*','finalseg/*','analyse/*','posseg/*']},

#     # 依赖包
#     install_requires=[
#         'requests >= 2.19.1',
#         "lxml >= 3.7.1",
#     ],
#     classifiers=[
#         # 'Development Status :: 4 - Beta',
#         # 'Operating System :: Microsoft'  # 你的操作系统  OS Independent      Microsoft
#         'Intended Audience :: Developers',
#         # 'License :: OSI Approved :: MIT License',
#         # 'License :: OSI Approved :: BSD License',  # BSD认证
#         'Programming Language :: Python',  # 支持的语言
#         'Programming Language :: Python :: 3',  # python版本 。。。
#         'Programming Language :: Python :: 3.4',
#         'Programming Language :: Python :: 3.5',
#         'Programming Language :: Python :: 3.6',
#         'Programming Language :: Python :: 3.7.3',
#         'Topic :: Software Development :: Libraries'
#     ],
#     zip_safe=True,
# )
from setuptools import setup, find_packages

setup(
    name = "scorepower",
    version = "0.1.1",
    keywords = ("pip", "scorepower"),
    description = "time and path tool",
    long_description = "time and path tool",
    license = "MIT Licence",

    url = "https://github.com/xxlest",
    author = "bruce",
    author_email = "85089081@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    py_modules=['scorepower'],
    install_requires = []
)