from selenium.webdriver.common.by import By
from base.basepage import BaseWebDriver


class BaiduPage(BaseWebDriver):
	""" 百度首页 """
	url = "https://www.baidu.com"

	kw = By.ID, "kw"
	su = By.ID, "su"

	def select(self, content):
		""" 百度搜索 """
		element_input = self.find_element(*self.kw,name="百度输入框")
		element_input.write(content)

		element_button = self.find_element(*self.su,name="百度一下按钮")
		element_button.click()


