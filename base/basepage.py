import time
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import allure
from common.logger.logger import logger


class BasePage:
	""" 基于selenium的二次封装 """

	def __init__(self, driver):
		"""
		初始化方法
		:param driver: driver对象
		:return: 无返回值
		driver示例：
			driver = webdriver.Firefox()
		"""
		try:
			self.driver = driver
			logger.debug("浏览器打开成功")
		except Exception as why:
			logger.error(f"浏览器打开失败，原因：{why}")
			raise Exception(why)

	def maximize_window(self):
		""" 浏览器最大化 """
		try:
			self.driver.maximize_window()
			logger.debug("浏览器最大化成功")
		except Exception as why:
			logger.error(f"浏览器最大化失败，原因{why}")
			self.save_screenshot()
			raise Exception(why)

	def get(self, url):
		"""
		访问url地址
		:param url: 要访问的url地址
		:return: 无返回值
		"""
		try:
			self.driver.get(url)
			logger.info(f"访问url：{url}成功")
			allure.attach(body=url, name="url", attachment_type=allure.attachment_type.TEXT)
		except Exception as why:
			logger.error(f"访问url：{url}失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def find_element(self, location: tuple, expected_conditions=None, timeout=10, **kwargs):
		"""
		查找单个元素
		:param location: 元素定位方式及表达式
		:param expected_conditions: 元素等待方式
		:param timeout: 元素等待超时时间
		:param kwargs: WebDriverWait对象的其它参数
		:return: 查找到的单个元素
		loc示例：
			loc = (By.XPATH,"//*[@id='kw']")
			loc = (Keys.CONTROL,"a")
			loc = (Keys.BACK_SPACE)
		expected_conditions示例：
			expected_conditions = EC.presence_of_element_located
			expected_conditions = EC.visibility_of_element_located
			expected_conditions = EC.element_to_be_clickable
		"""
		if not isinstance(location, tuple):
			msg = "loc must is tuple"
			raise Exception(msg)
		try:
			wait = WebDriverWait(driver=self.driver, timeout=timeout, **kwargs)
			method = expected_conditions or EC.presence_of_element_located
			elem = wait.until(method(location))
			logger.debug("元素找到")
			return elem
		except Exception as why:
			logger.error(f"元素未找到，原因；{why}")
			self.save_screenshot()
			raise Exception(why)

	def find_elements(self, location: tuple, expected_conditions=None, **kwargs):
		"""
			查找一组元素
			使用方法参考find_element方法
		"""
		elems = self.find_element(
			location=location, expected_conditions=expected_conditions or EC.presence_of_all_elements_located, **kwargs
		)
		return elems

	def write(self, *args, into, **kwargs):
		"""
		向输入框输入内容
		:param args: 要输入的内容
		:param into: 元素定位方式及表达式
		:param kwargs: find_element的其它参数
		:return: 无返回值
		"""
		try:
			elem = self.find_element(location=into, **kwargs)
			if args and all(args):
				ActionChains(driver=self.driver).click(elem).send_keys(*args).perform()
				logger.info(f"向输入框中输入内容成功")
			else:
				logger.info("未向输入框输入内容或向输入框中输入了不正确的内容")
		except Exception as why:
			logger.error(f"向输入框中输入内容失败，原因{why}")
			self.save_screenshot()
			raise Exception(why)

	def click(self, location, **kwargs):
		"""
		点击元素
		:param location: 元素定位方式及表达式
		:param kwargs: find_element的其它参数
		:return: 无返回值
		"""
		try:
			elem = self.find_element(
				location=location, expected_conditions=EC.element_to_be_clickable, **kwargs
			)
			elem.click()
			logger.info("元素点击成功")
		except Exception as why:
			logger.error(f"元素点击失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def clear(self, location, **kwargs):
		"""
		清除输入框中的内容
		:param location: 元素定位方式及表达式
		:param kwargs: find_element的其它参数
		:return: 无返回值
		"""
		try:
			elem = self.find_element(
				location=location, expected_conditions=EC.visibility_of_element_located, **kwargs
			)
			elem.clear()
			logger.info("输入框清除成功")
		except Exception as why:
			logger.error(f"输入框清除失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def switch_to_frame(self, location=None, **kwargs):
		"""
		切换到frame或退出frame loc为None时为退出frame,否则为进入frame
		:param location: 元素定位方式及表达式
		:param kwargs: find_element的其它参数
		:return: 无返回值
		"""
		try:
			if location:
				# 切换到frame
				self.find_element(
					location=location, expected_conditions=EC.frame_to_be_available_and_switch_to_it, **kwargs
				)
				logger.info("切换到frame成功")
			else:
				# 退出frame
				self.driver.switch_to.default_content()
				logger.info("退出frame成功")
		except Exception as why:
			self.save_screenshot()
			logger.error(f"切换或退出frame失败，原因：{why}")
			raise Exception(why)

	def switch_to_alert(self, send_keys=None, **kwargs):
		"""
		切换到弹窗 send_keys为None时为不输入内容，否则为输入内容
		:param send_keys: 要输入的内容
		:param kwargs: find_element的其它参数
		:return: 无返回值
		"""
		try:
			wait = WebDriverWait(driver=self.driver, **kwargs)
			wait.until(EC.alert_is_present())
			alert = self.driver.switch_to.alert
			if not alert:
				msg = "alert not found"
				logger.error("切换到弹窗失败，弹窗未发现。")
				raise Exception(msg)
			logger.info("切换到弹窗成功")
			if send_keys:
				alert.write(send_keys)
				logger.info("弹窗中输入内容成功")
			alert.accept()
			logger.info("弹窗已接受")
			return alert.text
		except Exception as why:
			logger.error(f"切换到弹窗失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def get_handles(self):
		""" 获取所有窗口句柄 """
		try:
			all_handles = self.driver.window_handles
			logger.debug("获取所有窗口句柄成功")
			return all_handles
		except Exception as why:
			logger.error(f"获取所有窗口句柄失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def switch_to_window(self, current_handles: list = None, handle=None, **kwargs):
		"""
		切换到新window或回到第一个window或到任意window
		如果current_handles传入窗口切换之前的所有窗口句柄，则切换到新打开的窗口。可通过get_handles方法获取所有
		窗口句柄。如果handle为None时，则切换到第一个被打开的窗口。如果handle传入窗口句柄时则切换到指定的窗口句柄
		:param current_handles: 窗口切换之前的所有窗口句柄
		:param handle: 要切换到的窗口句柄
		:param kwargs: find_element的其它参数
		:return: 无返回值
		"""
		try:
			if current_handles:
				if not isinstance(current_handles, list):
					msg = "current_handles must is a list"
					raise Exception(msg)
				wait = WebDriverWait(driver=self.driver, **kwargs)
				wait.until(EC.new_window_is_opened(current_handles))
				new_handles = self.get_handles()
				self.driver.switch_to.window(new_handles[-1])
				logger.info("切换到新窗口成功。")
				return
			if not handle:
				self.driver.switch_to.window(self.get_handles()[0])
				logger.info("切换到第一个窗口成功")
			else:
				self.driver.switch_to.window(handle)
				logger.info("切换到指定窗口成功")
		except Exception as why:
			logger.error(f"窗口切换失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def get_text(self, location, **kwargs):
		"""
		获取元素内文本
		:param location: 元素定位方式及表达式
		:param kwargs: find_element的其它参数
		:return: 元素内文本
		"""
		try:
			text = self.find_element(location=location, **kwargs).text
			logger.debug("获取元素内文本成功。")
			return text
		except Exception as why:
			logger.error(f"获取元素内文本失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def get_attribute(self, location, name, **kwargs):
		"""
		获取元素属性对应的文本值
		:param location: 元素定位方式及表达式
		:param name: 元素属性名
		:param kwargs: find_element的其它参数
		:return: 元素属性对应的文本值
		"""
		try:
			text = self.find_element(location=location, **kwargs).get_attribute(name)
			logger.debug(f"获取元素属性{name}文本成功。")
			return text
		except Exception as why:
			logger.error(f"获取元素属性{name}文本失败。原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def get_texts(self, location, **kwargs) -> list:
		"""
		获取一组元素的文本
		:param location: 元素定位方式及表达式
		:param kwargs: find_elements的其它参数
		:return: 一组元素文本列表
		"""
		try:
			elems = self.find_elements(location=location, **kwargs)
			texts = [elem.text for elem in elems]
			logger.debug("获取一组元素内文本成功。")
			return texts
		except Exception as why:
			logger.error(f"获取一组元素内文本失败。原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def get_attributes(self, location, name, **kwargs) -> list:
		"""
		获取一组元素属性对应的文本值
		:param location: 元素定位方式及表达式
		:param name: 元素属性名
		:param kwargs: find_elements的其它参数
		:return: 一组元素属性文本值列表
		"""
		try:
			elems = self.find_elements(location=location, **kwargs)
			texts = [elem.get_attribute(name) for elem in elems]
			logger.debug(f"获取一组元素属性{name}文本成功。")
			return texts
		except Exception as why:
			logger.error(f"获取一组元素属性{name}文本失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def select(self, location, value, method="index", **kwargs):
		"""
		select下拉框/复选框选择
		:param location: 元素定位方式及表达式
		:param value: method对应的值
		:param method: 选择方法，支持index、value、text
		:param kwargs: find_element的其它参数
		:return: 无返回值
		"""
		try:
			elem = self.find_element(location=location, **kwargs)
			sel = Select(elem)
			if method == "index":
				sel.select_by_index(value)
				logger.info("select下拉框/复选框元素根据index选择成功")
			elif method == "value":
				sel.select_by_value(value)
				logger.info("select下拉框/复选框元素根据value选择成功")
			elif method == "text":
				sel.select_by_visible_text(value)
				logger.info("select下拉框/复选框元素根据文本选择成功")
			else:
				msg = "method not supported"
				logger.error("select下拉框/复选框元素根据文本选择失败，选择方法不支持")
				raise Exception(msg)
		except Exception as why:
			logger.error(f"select下拉框/复选框元素根据文本选择失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def deselect_all(self, location, **kwargs):
		"""
		select下拉框/复选框取消所有选项
		:param location: 元素定位方式及表达式
		:param kwargs: find_element的其它参数
		:return: 无返回值
		"""
		try:
			elem = self.find_element(location=location, **kwargs)
			sel = Select(elem)
			sel.deselect_all()
			logger.info("select下拉框/复选框全部元素取消选择成功")
		except Exception as why:
			logger.info(f"select下拉框/复选框全部元素取消选择失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def checkbox_status(self, location, **kwargs) -> bool:
		""" 检查选择框元素状态 """
		try:
			result = self.find_element(location=location, **kwargs)
			logger.debug(f"检查选择框元素状态成功，元素状态为{'选择' if result else '未选择'}")
			return result
		except Exception as why:
			logger.debug(f"检查选择框元素状态失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def check_checkbox(self, location, **kwargs):
		"""
		选择选择框元素
		:param location: 元素定位方式及表达式
		:param kwargs: find_element的其它参数
		:return: 无返回值
		"""
		try:
			if not self.checkbox_status(location, **kwargs):
				self.click(location)
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

	def uncheck_checkbox(self, location, **kwargs):
		"""
		取消选择选择框元素
		:param location: 元素定位方式及表达式
		:param kwargs: find_element的其它参数
		:return: 无返回值
		"""
		try:
			if self.checkbox_status(location, **kwargs):
				self.click(location)
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
		filename = path.joinpath(time.strftime('%H%M%S') + ".png")
		try:
			self.driver.get_screenshot_as_file(filename)
			allure.attach(body=self.driver.get_screenshot_as_png(), name="image", attachment_type=allure.attachment_type.PNG)
			logger.debug(f"屏幕截图已保存，屏幕截图保存路径：{filename}")
		except Exception as why:
			logger.error(f"屏幕截图失败，原因：{why}")
			raise Exception(why)

	def elem_save_screenshot(self, location, **kwargs):
		""" 保存元素截图 """
		path = Path(__file__).resolve().parent.parent.joinpath("err_img", time.strftime('%Y-%m-%d'))
		path.mkdir(parents=True, exist_ok=True)
		filename = path.joinpath(time.strftime('elem_%H%M%S') + ".png")
		try:
			elem = self.find_element(location=location, **kwargs)
			elem.screenshot(filename)
			logger.debug(f"元素截图已保存，屏幕截图保存路径：{filename}")
		except Exception as why:
			logger.error(f"元素截图失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def click_by_js(self, location, **kwargs):
		"""
		点击元素
		:param location: 元素定位方式及表达式
		:param kwargs: find_element的其它参数
		:return: 无返回值
		"""
		try:
			elem = self.find_element(
				location=location, expected_conditions=EC.element_to_be_clickable, **kwargs
			)
			self.driver.execute_script("arguments[0].click();", elem)
			logger.info("元素点击成功")
		except Exception as why:
			logger.error(f"元素点击失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def scroll_into_view(self, location, **kwargs):
		"""
		滚动到元素可见位置
		:param location: 元素定位方式及表达式
		:param kwargs: find_element的其它参数
		:return: 无返回值
		"""
		try:
			elem = self.find_element(
				location=location, expected_conditions=EC.visibility_of_element_located, **kwargs
			)
			self.driver.execute_script("arguments[0].scrollIntoView(false);", elem)
			logger.debug("滚动到元素可见位置成功")
		except Exception as why:
			logger.error(f"滚动到元素可见位置失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def double_click(self, location, **kwargs):
		"""
		双击元素
		:param location: 元素定位方式及表达式
		:param kwargs: find_element的其它参数
		:return: 无返回值
		"""
		try:
			elem = self.find_element(
				location=location, **kwargs
			)
			ActionChains(driver=self.driver).double_click(elem).perform()
			logger.info("双击元素成功")
		except Exception as why:
			logger.error(f"双击元素失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def right_click(self, location, **kwargs):
		"""
		右击元素
		:param location: 元素定位方式及表达式
		:param kwargs: find_element的其它参数
		:return: 无返回值
		"""
		try:
			elem = self.find_element(
				location=location, **kwargs
			)
			ActionChains(driver=self.driver).context_click(elem).perform()
			logger.info("右击元素成功")
		except Exception as why:
			logger.error(f"右击元素失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def mouse_hover(self, location, **kwargs):
		"""
		在元素上悬停
		:param location: 元素定位方式及表达式
		:param kwargs: find_element的其它参数
		:return: 无返回值
		"""
		try:
			elem = self.find_element(
				location=location, **kwargs
			)
			ActionChains(driver=self.driver).move_to_element(elem).perform()
			logger.info("在元素上悬停成功")
		except Exception as why:
			logger.info(f"在元素上悬停失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def drag_and_drop_by_offset(self, location, xoffset, yoffset, **kwargs):
		"""
		将元素拖动到指定位置
		:param location: 元素定位方式及表达式
		:param xoffset: 目标位置x坐标
		:param yoffset: 目标位置y坐标
		:param kwargs: find_element的其它参数
		:return: 无返回值
		"""
		try:
			elem = self.find_element(
				location=location, **kwargs
			)
			ActionChains(driver=self.driver).drag_and_drop_by_offset(elem, xoffset, yoffset).perform()
			logger.info("将元素拖拽到指定位置成功")
		except Exception as why:
			logger.error(f"将元素拖拽到指定位置失败，原因：{why}")
			self.save_screenshot()
			raise Exception(why)

	def drag_and_drop(self, location_source, location_target, **kwargs):
		"""
		将元素拖动到另一个元素上
		:param location_source: 元素定位方式及表达式
		:param location_target: 拖动到的目标元素定位方式及表达式
		:param kwargs: find_element的其它参数
		:return: 无返回值
		"""
		try:
			source = self.find_element(
				location=location_source, **kwargs
			)
			target = self.find_element(
				location=location_target, **kwargs
			)
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
