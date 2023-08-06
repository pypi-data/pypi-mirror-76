from setuptools import setup

setup(
	name='msk_funcs',  # 需要打包的名字,即本模块要发布的名字
	version='v1.0',  # 版本
	description='some useful functions, welcome to use!',  # 简要描述
	py_modules=['common'],  # 需要打包的模块
	author='msk',  # 作者名
	author_email='solo_msk@163.com',  # 作者邮件
	url='https://github.com/solomsk/msk_funcs/',  # 项目地址,一般是代码托管的网站
	# requires=['requests','urllib3'], # 依赖包,如果没有,可以不要
	license='MIT'
)
