import pytest
from selenium.webdriver.common.by import By


class TestText:

	@pytest.fixture(scope="class", autouse=True)
	def goto(self, page):
		page.get("https://www.baidu.com")


	def test_text(self, page):
		location = By.CSS_SELECTOR, "span#s-usersetting-top"
		text = page.get_text(location)
		assert text == "设置"

	def test_attribute(self, page):
		location = By.ID, "su"
		text = page.get_attribute(location,"value")
		assert text == "百度一下"