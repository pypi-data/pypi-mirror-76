from distutils.core import setup
setup(
name='BZSuperMath20200816',     # 对外我们模块的名字
version='1.0',                # 版本号
description='这是第一个对外发布的模块，里面只有数学方法，用于测试哦',    # 描述
author='chenkui',            # 作者
author_email='chenk678@qq.com',          # 作者邮箱
py_modules=['BZSuperMath20200816.demo1','BZSuperMath20200816.demo2']     # 要发布的模块，不发布的不用写
)