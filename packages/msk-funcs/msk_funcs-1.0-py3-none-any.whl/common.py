#!/usr/bin/env python
# coding=utf-8
# 脚本功能：通用文件，常用函数定义
import datetime
import os
import time

# 获取当前文件名称
filetag = os.path.basename(__file__)
# 获取当前时间
curdate = str(time.strftime("%Y%m%d", time.localtime(time.time())))


def Log(str, filetag=filetag):
	'''
	日志函数
	:param str: 打印内容
	:param filetag: 打印本文件名称
	:return:无
	'''
	curtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	if not os.path.exists(work_path + "/logs"):
		os.makedirs(work_path + "/logs")
	log_obj = open(work_path + "/logs/sys_" + curdate + ".log", 'a+')
	log_obj.write(curtime + " [" + filetag + "] " + str + "\n")
	log_obj.flush()
	print(curtime + " [" + filetag + "] " + str + "\n")
	log_obj.close()


def timer(exeHour, func, sleepSec=3600):
	'''
	计时器函数
	:param exeHour: 几点（小时）执行
	:param func: 执行的函数
	:param sleepSec: 检测间隔，单位是秒
	:return:无
	'''
	while True:
		now_time = datetime.datetime.now()
		if now_time.hour == exeHour:
			Log('hour is ' + str(exeHour) + ', timer start to work!')
			func()
			Log('func exec complete!')
		# 每隔多少秒检测一次
		Log('timer start to sleep ' + str(sleepSec) + '..')
		time.sleep(sleepSec)


if __name__ == "__main__":
	pass
