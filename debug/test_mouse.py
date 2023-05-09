import pytest
from selenium.webdriver.common.by import By


class TestMouse:

	@pytest.fixture(scope="class", autouse=True)
	def goto(self, page):
		page.get("https://www.baidu.com")


	def test_mouse_hover(self, page):
		locator = By.XPATH, "//span[text()='设置']"
		element = page.find_element(*locator)
		element.mouse_hover()

	def test_right_click(self, page):
		locator = By.XPATH, "//span[text()='设置']"
		element = page.find_element(*locator)
		element.right_click()
