import pytest
from selenium.webdriver.common.by import By


class TestElement:

	@pytest.fixture(scope="class",autouse=True)
	def goto(self,page):
		page.get("https://www.baidu.com")

	def test_element(self, page):
		locator = By.ID, "su"
		element = page.find_element(*locator)
		assert element.get_attribute("value") == "百度一下"


