import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class TestMail:

	@pytest.fixture(scope="class", autouse=True)
	def goto(self, page):
		page.get("https://mail.163.com")

	def test_frame(self, page):
		locationFrame = By.CSS_SELECTOR, ".loginWrap  iframe"
		page.switch_to_frame(locationFrame)
		locationScanner = By.CSS_SELECTOR, "input[name='email']"
		elem = page.write("admin",into=locationScanner)
		assert elem.get_attribute("value") == "admin"
		page.switch_to_frame()
		locationButton = By.LINK_TEXT,"VIP"
		current_handles = page.driver.window_handles
		page.click(locationButton)
		WebDriverWait(page.driver,10).until(lambda x:len(x.window_handles) > len(current_handles))
		assert len(page.driver.window_handles) > len(current_handles)