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

	def baiduSelect(self, *args):
		""" 百度搜索 """
		if self.driver.current_url != self.url:
			self.driver.get(self.url)
		self.write(*args, into=self.kw,name="百度输入框")
		self.click(location=self.su,name="百度一下按钮")


