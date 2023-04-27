import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class TestClick:

	@pytest.fixture(scope="class", autouse=True)
	def goto(self, page):
		page.get("https://www.baidu.com")


	def test_click(self, page):
		locator1 = By.ID, "kw"
		element = page.find_element(*locator1)
		element.write("selenium")
		locator2 = By.ID, "su"
		element = page.find_element(*locator2)
		element.click()
		WebDriverWait(page.driver,10).until(lambda x: x.title != "百度一下，你就知道")
		assert page.driver.title == "selenium_百度搜索"