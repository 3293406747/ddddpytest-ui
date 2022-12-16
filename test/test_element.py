import pytest
from selenium.webdriver.common.by import By


class TestBaidu:

	@pytest.fixture(scope="class",autouse=True)
	def goto(self,page):
		page.get("https://www.baidu.com")

	def test_element(self, page):
		location = By.ID, "su"
		element = page.find_element(location)
		assert element.get_attribute("value") == "百度一下"

	def test_elements(self,page):
		location = By.CLASS_NAME,"input"
		elements = page.find_elements(location)
		assert isinstance(elements,list)


