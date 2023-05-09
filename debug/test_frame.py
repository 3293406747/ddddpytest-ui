import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class TestFrame:

	@pytest.fixture(scope="class", autouse=True)
	def goto(self, page):
		page.get("https://mail.163.com")

	def test_frame(self, page):
		locator_frame = By.CSS_SELECTOR, ".loginWrap  iframe"
		element1 = page.find_element(*locator_frame)
		element1.switch_to_frame()
		locator_scanner = By.CSS_SELECTOR, "input[name='email']"
		element2 = page.find_element(*locator_scanner)
		element2.write("admin")
		assert element2.get_attribute("value") == "admin"
		page.switch_to_default_frame()
		locator_button = By.LINK_TEXT,"VIP"
		current_handles = page.get_handles()
		element3 = page.find_element(*locator_button)
		element3.click()
		WebDriverWait(page.driver,10).until(lambda x:len(x.window_handles) > len(current_handles))
		assert len(page.driver.window_handles) > len(current_handles)
		page.switch_to_window(current_handles)