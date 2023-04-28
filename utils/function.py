import base64
import hashlib


def md5(string: str) -> str:
	""" md5加密函数 """
	if not isinstance(string, str):
		raise TypeError('input must be a string')
	encode = string.encode()
	return hashlib.md5(encode).hexdigest()


def bearer(string) -> str:
	""" base64加密函数 """
	if not isinstance(string, str):
		raise TypeError('input must be a string')
	return base64.b64encode(string.encode()).decode()
