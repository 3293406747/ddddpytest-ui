import random
import time

import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path

from utils.logger import logger

WAITED_DEFAULT_CONFIG = {
	"timeout": 10,
	"poll_frequency": 0.5,
	"ignored_exceptions": None
}


class BaseWebDriver:
	""" 基于selenium的二次封装 """

	def __init__(self, driver: WebDriver):
		"""
		初始化方法

		:param driver: driver对象
		:return: None

		示例：
			driver = webdriver.Firefox()
		"""
		self.driver = driver

	def maximize_window(self) -> None:
		"""
		浏览器最大化

		:return: None
		"""
		self.driver.maximize_window()
		logger.debug("浏览器最大化成功")

	def get(self, url, waited_method=None, waited_config: dict = None) -> None:
		"""
		访问url地址

		:param waited_config: 显示等待配置
		:param waited_method: 显示等待方法
		:param url: 要访问的url地址
		:return: None
		"""
		try:
			self.driver.get(url)
			if waited_method:
				wait = WebDriverWait(self.driver, **(waited_config or WAITED_DEFAULT_CONFIG))
				wait.until(waited_method)
			logger.debug(f"访问url：{url}成功")
			allure.attach(body=url, name="url", attachment_type=allure.attachment_type.TEXT)
		except Exception as why:
			logger.error(f"访问url：{url}失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def find_element(self, by=By.XPATH, value=None, name="", waited_config: dict = None):
		"""
		查找单个元素

		:param by: 定位方式
		:param value: 定位方式表达式
		:param waited_config: 显示等待配置
		:param name: 元素名称
		:return: 定位到的单个元素
		"""

		try:
			wait = WebDriverWait(self.driver, **(waited_config or WAITED_DEFAULT_CONFIG))
			method = EC.presence_of_element_located((by, value))
			element = wait.until(method)
			msg = f"要定位的元素{name}找到"
			logger.debug(msg)
			return BaseWebElement(element, self.driver, (by, value), name)
		except Exception as why:
			msg = f"要定位的元素{name}未找到，元素定位方式为:{by}表达式为:{value},原因:{why}"
			logger.error(msg)
			self.save_screenshot()
			raise Exception(msg)

	def switch_to_default_frame(self) -> None:
		"""
		退出frame

		:return: None
		"""
		try:
			self.driver.switch_to.default_content()
			msg = f"退出frame成功"
			allure.attach(msg, name="frame", attachment_type=allure.attachment_type.TEXT)
			logger.idebug(msg)
		except Exception as why:
			self.save_screenshot()
			msg = f"退出frame失败，原因:{why}"
			allure.attach(msg, name="frame", attachment_type=allure.attachment_type.TEXT)
			logger.error(msg)
			raise Exception(msg)

	def switch_to_alert(self, scanner=None, name="", waited_config: dict = None) -> None:
		"""
		切换到弹窗 scanner为None时为不输入内容，不为None时输入内容

		:param waited_config: 显示等待配置
		:param scanner: 要输入的内容
		:param name: 要定位的alert名称
		:return: None

		示例:
			switch_to_alert(scanner="测试",name="alert")
			switch_to_alert()
		"""
		try:
			wait = WebDriverWait(self.driver, **(waited_config or WAITED_DEFAULT_CONFIG))
			method = EC.alert_is_present()
			wait.until(method)
			# 切换到弹窗
			alert = self.driver.switch_to.alert
			if not alert:
				msg = f"切换到{name}弹窗元素失败，弹窗未发现。"
				logger.error(msg)
				allure.attach(msg, name="alert弹窗", attachment_type=allure.attachment_type.TEXT)
				raise Exception(msg)
			msg = f"切换到{name}弹窗元素成功"
			allure.attach(msg, name="alert弹窗", attachment_type=allure.attachment_type.TEXT)
			logger.idebug(msg)
			if scanner:
				# 向弹窗元素中输入内容
				alert.send_keys(scanner)
				msg = f"{name}弹窗元素中输入'{scanner}'成功"
				allure.attach(msg, name="alert弹窗", attachment_type=allure.attachment_type.TEXT)
				logger.idebug(msg)
			# 获取弹窗提示文本
			alerted_text = alert.text
			# 点击确认按钮
			alert.accept()
			msg = f"{name}弹窗元素已接受"
			allure.attach(msg, name="alert弹窗", attachment_type=allure.attachment_type.TEXT)
			logger.idebug(msg)
			return alerted_text
		except Exception as why:
			msg = f"{name}弹窗处理失败，原因:{why}"
			allure.attach(msg, name="alert弹窗", attachment_type=allure.attachment_type.TEXT)
			logger.error(msg)
			self.save_screenshot()
			raise Exception(msg)

	def get_handles(self) -> list:
		"""
		获取所有窗口句柄

		:return: 获取到的所有窗口句柄
		"""
		try:
			all_handles = self.driver.window_handles
			msg = "获取所有窗口句柄成功"
			logger.debug(msg)
			return all_handles
		except Exception as why:
			msg = f"获取所有窗口句柄失败，原因:{why}"
			logger.error(msg)
			self.save_screenshot()
			raise Exception(msg)

	def switch_to_window(self, handles: list = None, handle=None, name="", waited_config: dict = None):
		"""
		切换到新window或回到第一个window或到任意window
		如果current_handles传入窗口切换之前的所有窗口句柄，则切换到新打开的窗口。可通过get_handles方法获取所有
		窗口句柄。如果current_handles和handle均为None时，则切换到第一个被打开的窗口。如果current_handles为None
		且handle传入窗口句柄时则切换到指定的窗口句柄

		:param waited_config:
		:param handles: 窗口切换之前的所有窗口句柄
		:param handle: 要切换到的窗口句柄
		:param name: window窗口句柄名称
		:return: None

		示例:
			switch_to_window(get_handles())
			switch_to_window()
			switch_to_window(handle=get_handles()[0])
		"""
		try:
			if handles:
				# 切换到新窗口
				if not isinstance(handles, list):
					msg = "current_handles must be a list"
					raise Exception(msg)

				wait = WebDriverWait(self.driver, **(waited_config or WAITED_DEFAULT_CONFIG))
				method = EC.new_window_is_opened(handles)
				wait.until(method)
				handles = self.get_handles()
				self.driver.switch_to.window(handles[-1])
				msg = f"切换到新窗口成功。"
				allure.attach(msg, name="窗口", attachment_type=allure.attachment_type.TEXT)
				logger.idebug(msg)
			else:
				if not handle:
					# 切换到第一个窗口
					self.driver.switch_to.window(self.get_handles()[0])
					msg = f"切换到第一个窗口成功"
					allure.attach(msg, name="窗口", attachment_type=allure.attachment_type.TEXT)
					logger.idebug(msg)
				else:
					# 切换到指定窗口
					self.driver.switch_to.window(handle)
					msg = f"切换到窗口{name}成功"
					allure.attach(msg, name="窗口", attachment_type=allure.attachment_type.TEXT)
					logger.idebug(msg)
		except Exception as why:
			msg = f"窗口切换失败，原因:{why}"
			allure.attach(msg, name="窗口", attachment_type=allure.attachment_type.TEXT)
			logger.error(msg)
			self.save_screenshot()
			raise Exception(msg)

	def save_screenshot(self):
		""" 保存屏幕截图 """
		path = Path(__file__).resolve().parent.parent.joinpath("err_img", time.strftime('%Y-%m-%d'))
		path.mkdir(parents=True, exist_ok=True)
		filename = str(path.joinpath(time.strftime('%H%M%S') + str(random.randint(1, 100)) + ".png"))
		try:
			self.driver.get_screenshot_as_file(filename)
			allure.attach(body=self.driver.get_screenshot_as_png(), name="image",
						  attachment_type=allure.attachment_type.PNG)
			logger.debug(f"屏幕截图已保存，屏幕截图保存路径：{filename}")
		except Exception as why:
			logger.error(f"屏幕截图失败，原因：{why}")
			raise Exception(why)

	def close(self):
		""" 关闭当前窗口 """
		try:
			self.driver.close()
			logger.idebug("关闭当前窗口成功")
		except Exception as why:
			logger.error(f"关闭当前窗口失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def quit(self):
		""" 关闭浏览器 """
		try:
			self.driver.quit()
			logger.idebug("关闭浏览器成功")
		except Exception as why:
			logger.error(f"关闭浏览器失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)


class BaseWebElement:

	def __init__(self, element: WebElement, driver: WebDriver, locator: tuple, name: str = ""):
		self.element = element
		self.driver = driver
		self.locator = locator
		self.name = name

	def write(self, content):
		"""
		向输入框输入内容

		:param content: 要输入的内容
		:return: None

		示例:
			write("test",into=(By.ID, "test"),name="测试输入框")
			write(Keys.CONTROL,"a",into=(By.ID, "test"))
			write(Keys.ENTER,into=(By.ID, "test"))
		"""
		try:
			self.scroll_into_view()
			self.element.send_keys(content) if isinstance(content, str) else self.element.send_keys(*content)
			if isinstance(content, str):
				msg = f"向{self.name}元素中输入内容{content}成功"
				allure.attach(msg, name="输入", attachment_type=allure.attachment_type.TEXT)
				logger.idebug(msg)
		except Exception as why:
			msg = f"向元素{self.name}中输入内容失败，原因:{why}"
			allure.attach(msg, name="输入", attachment_type=allure.attachment_type.TEXT)
			logger.error(msg)
			self.save_screenshot()
			raise Exception(msg)

	def click(self, waited_config: dict = None):
		"""
		点击元素

		:return: None

		示例:
		click(location=(By.ID,"submit"),name="提交按钮")
		"""
		try:
			self.scroll_into_view()
			wait = WebDriverWait(self.driver, **(waited_config or WAITED_DEFAULT_CONFIG))
			method = EC.element_to_be_clickable(self.locator)
			wait.until(method)
			ActionChains(self.driver).move_to_element(self.element).click().perform()
			msg = f"元素{self.name}点击成功"
			allure.attach(msg, name="点击", attachment_type=allure.attachment_type.TEXT)
			logger.idebug(msg)
		except Exception as why:
			msg = f"元素{self.name}点击失败，原因:{why}"
			allure.attach(msg, name="点击", attachment_type=allure.attachment_type.TEXT)
			logger.error(msg)
			self.save_screenshot()
			raise Exception(msg)

	def clear(self):
		"""
		清除输入框中的内容

		:return: 无返回值

		示例:
			clear(location=(By.ID,"test"))
		"""
		try:
			self.scroll_into_view()
			self.element.clear()
			msg = f"元素{self.name}中内容清除成功"
			allure.attach(msg, name="清除", attachment_type=allure.attachment_type.TEXT)
			logger.idebug(msg)
		except Exception as why:
			msg = f"元素{self.name}中内容清除失败，原因:{why}"
			allure.attach(msg, name="清除", attachment_type=allure.attachment_type.TEXT)
			logger.error(msg)
			self.save_screenshot()
			raise Exception(msg)

	def switch_to_frame(self, waited_config: dict = None):
		"""
		切换到frame

		:waited_config:
		:return: 无返回值
		"""
		try:
			# 切换到frame
			wait = WebDriverWait(self.driver, **(waited_config or WAITED_DEFAULT_CONFIG))
			method = EC.frame_to_be_available_and_switch_to_it(self.locator)
			wait.until(method)
			msg = f"切换到{self.name}frame元素成功"
			allure.attach(msg, name="frame", attachment_type=allure.attachment_type.TEXT)
			logger.idebug(msg)
		except Exception as why:
			self.save_screenshot()
			msg = f"切换或退出{self.name}frame元素失败，原因:{why}"
			allure.attach(msg, name="frame", attachment_type=allure.attachment_type.TEXT)
			logger.error(msg)
			raise Exception(msg)

	def text(self):
		"""
		获取元素内文本

		:return: 定位到的元素内文本
		"""
		try:
			text = self.element.text
			msg = f"获取{self.name}元素内文本成功。"
			logger.debug(msg)
			return text
		except Exception as why:
			msg = f"获取{self.name}元素内文本失败，原因:{why}"
			logger.error(msg)
			self.save_screenshot()
			raise Exception(msg)

	def get_attribute(self, attribute):
		"""
		获取元素属性对应的文本值

		:param attribute: 要定位的元素的元素属性名
		:return: 元素属性内的文本值
		"""
		try:
			text = self.element.get_attribute(attribute)
			msg = f"获取{self.name}元素的{attribute}属性文本成功。"
			logger.debug(msg)
			return text
		except Exception as why:
			msg = f"获取{self.name}元素的{attribute}属性文本失败，原因:{why}"
			logger.error(msg)
			self.save_screenshot()
			raise Exception(msg)

	def scroll_into_view(self):
		"""
		滚动到元素可见位置

		:return: 无返回值
		"""
		try:
			self.driver.execute_script("arguments[0].scrollIntoView(false);", self.element)
			logger.debug("滚动到元素可见位置成功")
		except Exception as why:
			logger.error(f"滚动到元素可见位置失败，原因:{why}")
			self.save_screenshot()
			raise Exception(why)

	def select(self, value, method="index"):
		"""
		select下拉框/复选框选择

		:param value: method对应的值
		:param method: 选择方法，支持index、value、text
		:return: 无返回值
		"""
		try:
			self.scroll_into_view()
			select = Select(self.element)
			if method == "index":
				select.select_by_index(value)
				logger.idebug("select下拉框/复选框元素根据index选择成功")
			elif method == "value":
				select.select_by_value(value)
				logger.idebug("select下拉框/复选框元素根据value选择成功")
			elif method == "text":
				select.select_by_visible_text(value)
				logger.idebug("select下拉框/复选框元素根据文本选择成功")
			else:
				msg = "method not supported"
				logger.error("select下拉框/复选框元素根据文本选择失败，选择方法不支持")
				raise Exception(msg)
		except Exception as why:
			logger.error(f"select下拉框/复选框元素根据文本选择失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def deselect_all(self):
		"""
		select下拉框/复选框取消所有选项

		:return: 无返回值
		"""
		try:
			self.scroll_into_view()
			select = Select(self.element)
			select.deselect_all()
			logger.idebug("select下拉框/复选框全部元素取消选择成功")
		except Exception as why:
			logger.idebug(f"select下拉框/复选框全部元素取消选择失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def checkbox_status(self) -> bool:
		""" 检查选择框元素状态 """
		try:
			result = self.element.is_selected()
			logger.debug(f"检查选择框元素状态成功，元素状态为{'选择' if result else '未选择'}")
			return result
		except Exception as why:
			logger.debug(f"检查选择框元素状态失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def check_checkbox(self):
		"""
		选择选择框元素

		:return: 无返回值
		"""
		try:
			if not self.checkbox_status():
				self.click()
				logger.idebug("元素选择成功")
			else:
				logger.error("元素选择失败，元素已被选择")
				# self.save_screenshot()
				msg = "element has selected already"
				raise Exception(msg)
		except Exception as why:
			logger.error(f"元素选择失败，原因：{why}")
			# self.save_screenshot()
			raise Exception(why)

	def uncheck_checkbox(self):
		"""
		取消选择选择框元素

		:return: 无返回值
		"""
		try:
			if self.checkbox_status():
				self.click()
				logger.idebug("元素取消选择成功")
			else:
				logger.error("元素取消选择失败，元素未被选择")
				# self.save_screenshot()
				msg = "element has not selected already"
				raise Exception(msg)
		except Exception as why:
			logger.error(f"元素取消选择失败，原因：{why}")
			# self.save_screenshot()
			raise Exception(why)

	def save_screenshot(self):
		""" 保存元素截图 """
		path = Path(__file__).resolve().parent.parent.joinpath("err_img", time.strftime('%Y-%m-%d'))
		path.mkdir(parents=True, exist_ok=True)
		filename = str(path.joinpath(time.strftime('elem_%H%M%S') + str(random.randint(1, 100)) + ".png"))
		try:
			self.element.screenshot(filename)
			logger.debug(f"元素截图已保存，屏幕截图保存路径：{filename}")
		except Exception as why:
			logger.error(f"元素截图失败，原因：{why}")
			# self.save_screenshot()
			raise Exception(why)

	def click_by_js(self):
		"""
		用js点击元素

		:return: 无返回值
		"""
		try:
			self.driver.execute_script("arguments[0].click();", self.element)
			logger.idebug("元素点击成功")
		except Exception as why:
			logger.error(f"元素点击失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def double_click(self):
		"""
		双击元素

		:return: 无返回值
		"""
		try:
			ActionChains(driver=self.driver).move_to_element(self.element).double_click().perform()
			logger.idebug("双击元素成功")
		except Exception as why:
			logger.error(f"双击元素失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def right_click(self):
		"""
		右击元素

		:return: 无返回值
		"""
		try:
			ActionChains(driver=self.driver).context_click(self.element).perform()
			logger.idebug("右击元素成功")
		except Exception as why:
			logger.error(f"右击元素失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def mouse_hover(self):
		"""
		在元素上悬停

		:return: 无返回值
		"""
		try:
			ActionChains(driver=self.driver).move_to_element(self.element).perform()
			logger.idebug("在元素上悬停成功")
		except Exception as why:
			logger.idebug(f"在元素上悬停失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def drag_and_drop_by_offset(self, xoffset, yoffset):
		"""
		将元素拖动到指定位置

		:param xoffset: 目标位置x坐标
		:param yoffset: 目标位置y坐标
		:return: 无返回值
		"""
		try:
			ActionChains(driver=self.driver).drag_and_drop_by_offset(self.element, xoffset, yoffset).perform()
			logger.idebug("将元素拖拽到指定位置成功")
		except Exception as why:
			logger.error(f"将元素拖拽到指定位置失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def drag_and_drop(self, target_element):
		"""
		将元素拖动到另一个元素上

		:param target_element: 拖动到的目标元素
		:return: 无返回值
		"""
		try:
			ActionChains(driver=self.driver).drag_and_drop(self.element, target_element).perform()
			logger.idebug("将元素拖拽到另一个元素上成功")
		except Exception as why:
			logger.error(f"将元素拖拽到另一个元素上失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)
