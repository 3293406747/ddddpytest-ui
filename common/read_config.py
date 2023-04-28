from functools import lru_cache
from pathlib import Path
from utils.read_yaml import read_yaml

BASE_PATH = Path(__file__).resolve().parent.parent

@lru_cache(None)		# 缓存
def read_config(filename="local.yaml", encoding="utf-8") ->dict:
	""" 读取配置文件 """
	return read_yaml(filename=str(BASE_PATH.joinpath("config", filename)), encoding=encoding)
