import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


class TestWrite:

	@pytest.fixture(scope="class", autouse=True)
	def goto(self, page):
		page.get("https://www.baidu.com")

	def test_write(self, page):
		location = By.ID, "kw"
		element = page.write("selenium", into=location, msg="百度搜索")
		assert element.get_attribute("value") == "selenium"

	def test_write_keys(self, page):
		location = By.ID, "kw"
		page.write(Keys.CONTROL, "a", into=location)
		element = page.write(Keys.BACK_SPACE, into=location)
		assert element.get_attribute("value") == ""