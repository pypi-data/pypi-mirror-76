# -*- encoding: UTF-8 -*-
from setuptools import setup, find_packages
import io

VERSION = '1.12.1'

with io.open("README.md", encoding='utf-8') as f:
    long_description = f.read()

#install_requires = open("requires.txt").readlines()

setup(
    name="pgabc",  # pip 安装时用的名字
    version="1.12.1",  # 当前版本，每次更新上传到pypi都需要修改
    author="WangMin",
    author_email="pgabc@sina.com",
    url="https://github.com/HewayPg",
    keywords="indicator",
    description="Data calulation",
    long_description=long_description,
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    license='MIT License',
    classifiers=[], install_requires=[],

)






