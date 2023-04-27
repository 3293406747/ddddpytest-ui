import pytest
from selenium.webdriver.common.by import By


class TestClear:

	@pytest.fixture(scope="class",autouse=True)
	def goto(self,page):
		page.get("https://www.baidu.com")

	def test_clear(self, page):
		locator = By.ID, "kw"
		element = page.find_element(*locator)
		element.write("selenium")
		assert element.get_attribute("value") == "selenium"
		element.clear()
		assert element.get_attribute("value") == ""