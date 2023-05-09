import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestJs:

	@pytest.fixture(scope="class", autouse=True)
	def goto(self, page):
		page.get("http://news.baidu.com")


	def test_scroll(self, page):
		locator1 = By.XPATH, "//a[text()='切换城市']"
		element1 = page.find_element(*locator1)
		element1.scroll_into_view()
		locator2 = By.XPATH, "//a[text()='热点要闻']"
		element2 = page.find_element(*locator2)
		element2.scroll_into_view()

	def test_click_js(self,page):
		locator = By.ID, "s_btn_wr"
		current_url = page.driver.current_url
		element = page.find_element(*locator)
		element.click()
		WebDriverWait(page.driver,timeout=10).until(EC.url_changes(current_url))
		assert page.driver.current_url == "https://www.baidu.com/?tn=news"
