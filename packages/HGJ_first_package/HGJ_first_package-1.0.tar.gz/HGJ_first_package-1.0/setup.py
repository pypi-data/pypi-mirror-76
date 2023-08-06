from distutils.core import setup
setup(
name='HGJ_first_package',
# 对外我们模块的名字
version='1.0', # 版本号
description='This is the first package that I pulish in the website, THX',
#描述
author='Huang Guangji', # 作者
author_email='976824193@qq.com',
py_modules=['moduleA','moduleB'] # 要发布的模块
)