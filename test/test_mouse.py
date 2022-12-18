import pytest
from selenium.webdriver.common.by import By


class TestMouse:

	@pytest.fixture(scope="class", autouse=True)
	def goto(self, page):
		page.get("https://www.baidu.com")


	def test_mouse_hover(self, page):
		location = By.XPATH, "//span[text()='设置']"
		page.mouse_hover(location)

	def test_right_click(self, page):
		location = By.XPATH, "//span[text()='设置']"
		page.right_click(location)
