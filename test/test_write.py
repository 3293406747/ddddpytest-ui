from selenium.webdriver.common.by import By


class TestBaidu:

	def test_write(self, page):
		location = By.ID, "kw"
		element = page.write("selenium",into=location)
		assert element.get_attribute("value") == "selenium"
		page.clear(location)