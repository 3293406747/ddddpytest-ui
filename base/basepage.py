import random
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from pathlib import Path
import allure
from utils.logger import logger


class BasePage:
	""" 基于selenium的二次封装 """

	def __init__(self, driver: WebDriver):
		"""
		初始化方法

		:param driver: driver对象
		:return: 无返回值

		示例：
			driver = webdriver.Firefox()
		"""
		self.driver = driver

	def maximize_window(self):
		"""
		浏览器最大化
		:return: 无返回值
		"""
		try:
			self.driver.maximize_window()
			logger.debug("浏览器最大化成功")
		except Exception as why:
			msg = f"浏览器最大化失败，原因:{why}"
			logger.error(msg)
			self.save_screenshot()
			raise Exception(msg)

	def wait(self, timeout=10, poll_frequency=0.5, *args, **kwargs):
		return WebDriverWait(driver=self.driver, timeout=timeout, poll_frequency=poll_frequency, *args, **kwargs)

	@property
	def EC(self):
		return expected_conditions

	def get(self, url, waited_method=None, waited_time=10, waited_poll_frequency=0.5):
		"""
		访问url地址

		:param waited_time:
		:param waited_poll_frequency:
		:param waited_method:
		:param url: 要访问的url地址
		:return: 无返回值
		"""
		try:
			self.driver.get(url)
			if waited_method:
				# self.EC.url_contains(url)
				wait = self.wait(timeout=waited_time, poll_frequency=waited_poll_frequency)
				wait.until(waited_method)
			logger.debug(f"访问url：{url}成功")
			allure.attach(body=url, name="url", attachment_type=allure.attachment_type.TEXT)
		except Exception as why:
			logger.error(f"访问url：{url}失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def find_element(self, locator: tuple, waited_timeout=10, waited_poll_frequency=0.5, name="") -> WebElement:
		"""
		查找单个元素

		:param waited_poll_frequency:
		:param waited_timeout:
		:param locator: 元素定位方式及表达式
		:param name: 元素名称
		:return: 定位到的单个元素

		location示例：
			location = (By.XPATH,"//*[@id='kw']")
		expected_conditions示例：
			expected_conditions = EC.presence_of_element_located
			expected_conditions = EC.visibility_of_element_located
			expected_conditions = EC.element_to_be_clickable
		示例:
			location = (By.XPATH,"//*[@id='kw']")
			find_element(location)
		"""
		if not isinstance(locator, tuple):
			msg = "location must be a tuple"
			raise Exception(msg)

		try:
			wait = self.wait(timeout=waited_timeout, poll_frequency=waited_poll_frequency)
			method = self.EC.presence_of_element_located(locator)
			element = wait.until(method)
			msg = f"要定位的元素{name}找到"
			logger.debug(msg)
			return element
		except Exception as why:
			msg = f"要定位的元素{name}未找到，元素定位方式为:{locator[0]}表达式为:{locator[1]},原因:{why}"
			logger.error(msg)
			self.save_screenshot()
			raise Exception(msg)

	def write(self, content, locator: tuple, name=""):
		"""
		向输入框输入内容

		:param content: 要输入的内容
		:param locator: 元素定位方式及表达式
		:param name: 要定位的输入框元素名称
		:return: 定位的输入框元素

		示例:
			write("test",into=(By.ID, "test"),name="测试输入框")
			write(Keys.CONTROL,"a",into=(By.ID, "test"))
			write(Keys.ENTER,into=(By.ID, "test"))
		"""
		try:
			element = self.find_element(locator=locator, name=name)
			self.scroll_into_view(locator)
			element.send_keys(content) if isinstance(content, str) else element.send_keys(*content)
			if isinstance(content, str):
				msg = f"向{name}元素中输入内容{content}成功"
				allure.attach(msg, name="输入", attachment_type=allure.attachment_type.TEXT)
				logger.info(msg)
			return element
		except Exception as why:
			msg = f"向元素{name}中输入内容失败，原因:{why}"
			allure.attach(msg, name="输入", attachment_type=allure.attachment_type.TEXT)
			logger.error(msg)
			self.save_screenshot()
			raise Exception(msg)

	def click(self, locator, name=""):
		"""
		点击元素

		:param locator: 元素定位方式及表达式
		:param name: 要点击的元素名称
		:return: 点击的元素

		示例:
		click(location=(By.ID,"submit"),name="提交按钮")
		"""
		try:
			element = self.find_element(locator=locator, name=name)
			self.scroll_into_view(locator)
			wait = self.wait()
			method = self.EC.element_to_be_clickable(locator)
			wait.until(method)
			ActionChains(self.driver).move_to_element(element).click().perform()
			msg = f"元素{name}点击成功"
			allure.attach(msg, name="点击", attachment_type=allure.attachment_type.TEXT)
			logger.info(msg)
			return element
		except Exception as why:
			msg = f"元素{name}点击失败，原因:{why}"
			allure.attach(msg, name="点击", attachment_type=allure.attachment_type.TEXT)
			logger.error(msg)
			self.save_screenshot()
			raise Exception(msg)

	def clear(self, locator, name=""):
		"""
		清除输入框中的内容

		:param locator: 元素定位方式及表达式
		:param name: 要清除的元素名称
		:return: 无返回值

		示例:
        	clear(location=(By.ID,"test"))
        """
		try:
			element = self.find_element(locator=locator, name=name)
			self.scroll_into_view(locator)
			element.clear()
			msg = f"元素{name}中内容清除成功"
			allure.attach(msg, name="清除", attachment_type=allure.attachment_type.TEXT)
			logger.info(msg)
		except Exception as why:
			msg = f"元素{name}中内容清除失败，原因:{why}"
			allure.attach(msg, name="清除", attachment_type=allure.attachment_type.TEXT)
			logger.error(msg)
			self.save_screenshot()
			raise Exception(msg)

	def switch_to_frame(self, locator=None, name=""):
		"""
		切换到frame或退出frame location为None时为退出frame,不为None为进入frame

		:param locator: 元素定位方式及表达式
		:param name: 要定位的frame元素名称
		:return: 无返回值

		示例:
			switch_to_frame(location=(By.ID,"test"),name="测试")
			switch_to_frame()
		"""
		try:
			if locator is not None:
				# 切换到frame
				self.find_element(locator=locator, name=name)
				wait = self.wait()
				method = self.EC.frame_to_be_available_and_switch_to_it(locator)
				wait.until(method)
				msg = f"切换到{name}frame元素成功"
				allure.attach(msg, name="frame", attachment_type=allure.attachment_type.TEXT)
				logger.info(msg)
			else:
				# 退出frame
				self.driver.switch_to.default_content()
				msg = f"退出{name}frame元素成功"
				allure.attach(msg, name="frame", attachment_type=allure.attachment_type.TEXT)
				logger.info(msg)
		except Exception as why:
			self.save_screenshot()
			msg = f"切换或退出{name}frame元素失败，原因:{why}"
			allure.attach(msg, name="frame", attachment_type=allure.attachment_type.TEXT)
			logger.error(msg)
			raise Exception(msg)

	def switch_to_alert(self, scanner=None, name=""):
		"""
		切换到弹窗 scanner为None时为不输入内容，不为None时输入内容

		:param scanner: 要输入的内容
		:param name: 要定位的alert名称
		:return: 无返回值

		示例:
			switch_to_alert(scanner="测试",name="alert")
			switch_to_alert()
		"""
		try:
			wait = self.wait()
			method = self.EC.alert_is_present()
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
			logger.info(msg)
			if scanner:
				# 向弹窗元素中输入内容
				alert.send_keys(scanner)
				msg = f"{name}弹窗元素中输入'{scanner}'成功"
				allure.attach(msg, name="alert弹窗", attachment_type=allure.attachment_type.TEXT)
				logger.info(msg)
			# 获取弹窗提示文本
			alerted_text = alert.text
			# 点击确认按钮
			alert.accept()
			msg = f"{name}弹窗元素已接受"
			allure.attach(msg, name="alert弹窗", attachment_type=allure.attachment_type.TEXT)
			logger.info(msg)
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

	def switch_to_window(self, handles: list = None, handle=None, name=""):
		"""
		切换到新window或回到第一个window或到任意window
		如果current_handles传入窗口切换之前的所有窗口句柄，则切换到新打开的窗口。可通过get_handles方法获取所有
		窗口句柄。如果current_handles和handle均为None时，则切换到第一个被打开的窗口。如果current_handles为None
		且handle传入窗口句柄时则切换到指定的窗口句柄

		:param handles: 窗口切换之前的所有窗口句柄
		:param handle: 要切换到的窗口句柄
		:param name: window窗口句柄名称
		:return: 无返回值

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

				wait = self.wait()
				method = self.EC.new_window_is_opened(handles)
				wait.until(method)
				handles = self.get_handles()
				self.driver.switch_to.window(handles[-1])
				msg = f"切换到新窗口成功。"
				allure.attach(msg, name="窗口", attachment_type=allure.attachment_type.TEXT)
				logger.info(msg)
			else:
				if not handle:
					# 切换到第一个窗口
					self.driver.switch_to.window(self.get_handles()[0])
					msg = f"切换到第一个窗口成功"
					allure.attach(msg, name="窗口", attachment_type=allure.attachment_type.TEXT)
					logger.info(msg)
				else:
					# 切换到指定窗口
					self.driver.switch_to.window(handle)
					msg = f"切换到窗口{name}成功"
					allure.attach(msg, name="窗口", attachment_type=allure.attachment_type.TEXT)
					logger.info(msg)
		except Exception as why:
			msg = f"窗口切换失败，原因:{why}"
			allure.attach(msg, name="窗口", attachment_type=allure.attachment_type.TEXT)
			logger.error(msg)
			self.save_screenshot()
			raise Exception(msg)

	def get_text(self, locator, name=""):
		"""
		获取元素内文本

		:param locator: 元素定位方式及表达式
		:param name: 要定位的元素名称
		:return: 定位到的元素内文本
		"""
		try:
			element = self.find_element(locator=locator, name=name)
			text = element.text
			msg = f"获取{name}元素内文本成功。"
			logger.debug(msg)
			return text
		except Exception as why:
			msg = f"获取{name}元素内文本失败，原因:{why}"
			logger.error(msg)
			self.save_screenshot()
			raise Exception(msg)

	def get_attribute(self, locator, attribute, name=""):
		"""
		获取元素属性对应的文本值

		:param locator: 元素定位方式及表达式
		:param attribute: 要定位的元素的元素属性名
		:param name: 要定位的元素名称
		:return: 元素属性内的文本值
		"""
		try:
			element = self.find_element(locator=locator, name=name)
			text = element.get_attribute(attribute)
			msg = f"获取{name}元素的{attribute}属性文本成功。"
			logger.debug(msg)
			return text
		except Exception as why:
			msg = f"获取{name}元素的{attribute}属性文本失败，原因:{why}"
			logger.error(msg)
			self.save_screenshot()
			raise Exception(msg)

	def select(self, locator, value, method="index"):
		"""
		select下拉框/复选框选择

		:param locator: 元素定位方式及表达式
		:param value: method对应的值
		:param method: 选择方法，支持index、value、text
		:return: 无返回值
		"""
		try:
			element = self.find_element(locator=locator)
			self.scroll_into_view(locator)
			select = Select(element)
			if method == "index":
				select.select_by_index(value)
				logger.info("select下拉框/复选框元素根据index选择成功")
			elif method == "value":
				select.select_by_value(value)
				logger.info("select下拉框/复选框元素根据value选择成功")
			elif method == "text":
				select.select_by_visible_text(value)
				logger.info("select下拉框/复选框元素根据文本选择成功")
			else:
				msg = "method not supported"
				logger.error("select下拉框/复选框元素根据文本选择失败，选择方法不支持")
				raise Exception(msg)
		except Exception as why:
			logger.error(f"select下拉框/复选框元素根据文本选择失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def deselect_all(self, locator):
		"""
		select下拉框/复选框取消所有选项

		:param locator: 元素定位方式及表达式
		:return: 无返回值
		"""
		try:
			element = self.find_element(locator=locator)
			self.scroll_into_view(locator)
			select = Select(element)
			select.deselect_all()
			logger.info("select下拉框/复选框全部元素取消选择成功")
		except Exception as why:
			logger.info(f"select下拉框/复选框全部元素取消选择失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def checkbox_status(self, locator) -> bool:
		""" 检查选择框元素状态 """
		try:
			element = self.find_element(locator=locator)
			result = element.is_selected()
			logger.debug(f"检查选择框元素状态成功，元素状态为{'选择' if result else '未选择'}")
			return result
		except Exception as why:
			logger.debug(f"检查选择框元素状态失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def check_checkbox(self, locator):
		"""
		选择选择框元素

		:param locator: 元素定位方式及表达式
		:return: 无返回值
		"""
		try:
			if not self.checkbox_status(locator):
				self.click(locator)
				logger.info("元素选择成功")
			else:
				logger.error("元素选择失败，元素已被选择")
				self.save_screenshot()
				msg = "element has selected already"
				raise Exception(msg)
		except Exception as why:
			logger.error(f"元素选择失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def uncheck_checkbox(self, locator):
		"""
		取消选择选择框元素

		:param locator: 元素定位方式及表达式
		:return: 无返回值
		"""
		try:
			if self.checkbox_status(locator):
				self.click(locator)
				logger.info("元素取消选择成功")
			else:
				logger.error("元素取消选择失败，元素未被选择")
				self.save_screenshot()
				msg = "element has not selected already"
				raise Exception(msg)
		except Exception as why:
			logger.error(f"元素取消选择失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

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

	def elem_save_screenshot(self, locator, **kwargs):
		""" 保存元素截图 """
		path = Path(__file__).resolve().parent.parent.joinpath("err_img", time.strftime('%Y-%m-%d'))
		path.mkdir(parents=True, exist_ok=True)
		filename = str(path.joinpath(time.strftime('elem_%H%M%S') + str(random.randint(1, 100)) + ".png"))
		try:
			element = self.find_element(locator=locator, **kwargs)
			element.screenshot(filename)
			logger.debug(f"元素截图已保存，屏幕截图保存路径：{filename}")
		except Exception as why:
			logger.error(f"元素截图失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def click_by_js(self, locator):
		"""
		用js点击元素

		:param locator: 元素定位方式及表达式
		:return: 无返回值
		"""
		try:
			element = self.find_element(locator=locator)
			self.driver.execute_script("arguments[0].click();", element)
			logger.info("元素点击成功")
		except Exception as why:
			logger.error(f"元素点击失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def scroll_into_view(self, locator):
		"""
		滚动到元素可见位置

		:param locator: 元素定位方式及表达式
		:return: 无返回值
		"""
		try:
			element = self.find_element(locator=locator)
			self.driver.execute_script("arguments[0].scrollIntoView(false);", element)
			logger.debug("滚动到元素可见位置成功")
		except Exception as why:
			logger.error(f"滚动到元素可见位置失败，原因:{why}")
			self.save_screenshot()
			raise Exception(why)

	def double_click(self, locator):
		"""
		双击元素

		:param locator: 元素定位方式及表达式
		:return: 无返回值
		"""
		try:
			element = self.find_element(locator=locator)
			ActionChains(driver=self.driver).move_to_element(element).double_click().perform()
			logger.info("双击元素成功")
		except Exception as why:
			logger.error(f"双击元素失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def right_click(self, locator):
		"""
		右击元素

		:param locator: 元素定位方式及表达式
		:return: 无返回值
		"""
		try:
			element = self.find_element(locator=locator)
			ActionChains(driver=self.driver).context_click(element).perform()
			logger.info("右击元素成功")
		except Exception as why:
			logger.error(f"右击元素失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def mouse_hover(self, locator):
		"""
		在元素上悬停

		:param locator: 元素定位方式及表达式
		:return: 无返回值
		"""
		try:
			element = self.find_element(locator=locator)
			ActionChains(driver=self.driver).move_to_element(element).perform()
			logger.info("在元素上悬停成功")
		except Exception as why:
			logger.info(f"在元素上悬停失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def drag_and_drop_by_offset(self, locator, xoffset, yoffset):
		"""
		将元素拖动到指定位置

		:param locator: 元素定位方式及表达式
		:param xoffset: 目标位置x坐标
		:param yoffset: 目标位置y坐标
		:return: 无返回值
		"""
		try:
			element = self.find_element(locator=locator)
			ActionChains(driver=self.driver).drag_and_drop_by_offset(element, xoffset, yoffset).perform()
			logger.info("将元素拖拽到指定位置成功")
		except Exception as why:
			logger.error(f"将元素拖拽到指定位置失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def drag_and_drop(self, locator_source, locator_target):
		"""
		将元素拖动到另一个元素上

		:param locator_source: 元素定位方式及表达式
		:param locator_target: 拖动到的目标元素定位方式及表达式
		:return: 无返回值
		"""
		try:
			source = self.find_element(locator=locator_source)
			target = self.find_element(locator=locator_target)
			ActionChains(driver=self.driver).drag_and_drop(source, target).perform()
			logger.info("将元素拖拽到另一个元素上成功")
		except Exception as why:
			logger.error(f"将元素拖拽到另一个元素上失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def close(self):
		""" 关闭当前窗口 """
		try:
			self.driver.close()
			logger.info("关闭当前窗口成功")
		except Exception as why:
			logger.error(f"关闭当前窗口失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def quit(self):
		""" 关闭浏览器 """
		try:
			self.driver.quit()
			logger.info("关闭浏览器成功")
		except Exception as why:
			logger.error(f"关闭浏览器失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)
