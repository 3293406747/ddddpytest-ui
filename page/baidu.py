from selenium.webdriver.common.by import By
from base.basepage import BaseWebDriver


class BaiduPage(BaseWebDriver):
	""" 百度首页 """
	# 访问地址
	url = "https://www.baidu.com"
	# 百度搜索输入框
	kw = By.ID, "kw"
	# 百度一下按钮
	su = By.ID, "su"

	def select(self, content):
		""" 百度搜索 """
		element_input = self.find_element(*self.kw,name="百度输入框")
		element_input.write(content)
		element_button = self.find_element(*self.su,name="百度一下按钮")
		element_button.click()


