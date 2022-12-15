from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class TestBaidu:

	def test_write(self, page):
		location1 = By.ID, "kw"
		page.write("selenium",into=location1)
		location2 = By.ID, "su"
		page.click(location2)
		WebDriverWait(page.driver,10).until(lambda x: x.title != "百度一下，你就知道")
		assert page.driver.title == "selenium_百度搜索"
		page.clear(location1)