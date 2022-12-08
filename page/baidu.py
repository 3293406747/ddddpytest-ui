from selenium.webdriver.common.by import By
from base.basepage import BasePage


class BaiduPage(BasePage):
	""" 百度首页 """
	# 访问地址
	url = "https://www.baidu.com"
	# 百度搜索输入框
	kw = By.ID, "kw"
	# 百度一下按钮
	su = By.ID, "su"

	def baidu_select(self,text=None):
		""" 百度搜索 """
		try:
			self.write(text, into=self.kw) if text else ...
			self.click(location=self.su)
		except Exception as why:
			self.quit()
			raise Exception(why)


