import pytest
from selenium.webdriver.common.by import By


class TestWindow:

	@pytest.fixture(scope="class",autouse=True)
	def goto(self,page):
		page.get("https://www.baidu.com")

	def test_window_new(self, page):
		location = By.LINK_TEXT, "新闻"
		currentHandles = page.get_handles()
		page.click(location)
		page.switch_to_window(current_handles=currentHandles)
		assert page.driver.current_url == "http://news.baidu.com/"

	def test_window_default(self, page):
		page.switch_to_window()
		assert page.driver.current_url == "https://www.baidu.com/"

	def test_window(self, page):
		currentHandles = page.get_handles()
		page.switch_to_window(handle=currentHandles[-1])
		assert page.driver.current_url == "http://news.baidu.com/"
