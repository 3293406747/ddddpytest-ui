import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


class TestWrite:

	@pytest.fixture(scope="class", autouse=True)
	def goto(self, page):
		page.get("https://www.baidu.com")

	def test_write(self, page):
		locator = By.ID, "kw"
		element = page.find_element(*locator)
		element.write("selenium")
		assert element.get_attribute("value") == "selenium"

	def test_write_keys(self, page):
		locator = By.ID, "kw"
		element = page.find_element(*locator)
		element.write(content=(Keys.CONTROL, "a"))
		element.write(Keys.BACK_SPACE)
		assert element.get_attribute("value") == ""