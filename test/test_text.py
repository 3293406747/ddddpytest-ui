import pytest
from selenium.webdriver.common.by import By


class TestText:

	@pytest.fixture(scope="class", autouse=True)
	def goto(self, page):
		page.get("https://www.baidu.com")


	def test_text(self, page):
		locator = By.CSS_SELECTOR, "span#s-usersetting-top"
		element = page.find_element(*locator)
		text = element.text()
		assert text == "设置"

	def test_attribute(self, page):
		locator = By.ID, "su"
		element = page.find_element(*locator)
		text = element.get_attribute("value")
		assert text == "百度一下"