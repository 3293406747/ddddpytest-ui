import pytest
from selenium.webdriver.common.by import By


class TestBaidu:

	@pytest.fixture(scope="class", autouse=True)
	def goto(self, page):
		page.get("https://www.baidu.com")

	def test_save_screenshot(self,page):
		page.save_screenshot()

	def test_elem_save_screenshot(self, page):
		location = By.ID, "su"
		page.elem_save_screenshot(location)