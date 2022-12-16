import pytest
from selenium.webdriver.common.by import By


class TestBaidu:

	@pytest.fixture(scope="class",autouse=True)
	def goto(self,page):
		page.get("https://www.baidu.com")

	def test_clear(self, page):
		location = By.ID, "kw"
		element = page.write("selenium",into=location)
		assert element.get_attribute("value") == "selenium"
		page.clear(location)
		assert element.get_attribute("value") == ""