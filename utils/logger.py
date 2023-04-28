"""
logger日志
"""
import sys,time
from loguru import logger as logging
from common.read_config import read_config


class Logger:
	""" 日志管理 """
	def __init__(self):
		self.logger = logging
		self.logger.remove()
		# 控制台日志
		self.logger.add(
			sink=sys.stderr,
			**read_config()["logger"]["console"],
		)
	# 文件日志
		self.logger.add(
			sink = f'./logs/{time.strftime("%Y-%m-%d")}/log_{time.strftime("%H_%M_%S")}.log',
			**read_config()["logger"]["file"],
		)
		# 文件错误日志
		self.logger.add(
			sink=f'./logs/{time.strftime("%Y-%m-%d")}/error.log',
			**read_config()["logger"]["errorFile"],
		)


logger = Logger().logger
logger.debug('日志启动成功')