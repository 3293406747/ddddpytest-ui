import pytest
from selenium.webdriver.common.by import By


class TestWindow:

	@pytest.fixture(scope="class",autouse=True)
	def goto(self,page):
		page.get("http://www.baidu.com")

	def test_window_new(self, page):
		locator = By.LINK_TEXT, "新闻"
		handles = page.get_handles()
		page.click(locator)
		page.switch_to_window(handles=handles)
		wait = page.wait()
		method = page.EC.url_to_be("about:blank")
		wait.until_not(method)
		assert page.driver.current_url == "https://news.baidu.com/"

	def test_window(self, page):
		currentHandles = page.get_handles()
		page.switch_to_window(handle=currentHandles[-1])
		wait = page.wait()
		method = page.EC.url_to_be("about:blank")
		wait.until_not(method)
		assert page.driver.current_url == "https://news.baidu.com/"
