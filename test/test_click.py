import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class TestClick:

	@pytest.fixture(scope="class", autouse=True)
	def goto(self, page):
		page.get("https://www.baidu.com")


	def test_click(self, page):
		location1 = By.ID, "kw"
		page.write("selenium", locator=location1)
		location2 = By.ID, "su"
		page.click(location2)
		WebDriverWait(page.driver,10).until(lambda x: x.title != "百度一下，你就知道")
		assert page.driver.title == "selenium_百度搜索"