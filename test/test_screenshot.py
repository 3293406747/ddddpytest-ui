import pytest
from selenium.webdriver.common.by import By


class TestScreenshot:

	@pytest.fixture(scope="class", autouse=True)
	def goto(self, page):
		page.get("https://www.baidu.com")

	def test_save_screenshot(self,page):
		page.save_screenshot()

	def test_elem_save_screenshot(self, page):
		locator = By.ID, "su"
		element = page.find_element(*locator)
		element.save_screenshot()