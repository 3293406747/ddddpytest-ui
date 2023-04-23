import pytest
from selenium.webdriver.common.by import By


class TestJs:

	@pytest.fixture(scope="class", autouse=True)
	def goto(self, page):
		page.get("http://news.baidu.com")


	def test_scroll(self, page):
		location = By.XPATH, "//a[text()='切换城市']"
		page.scroll_into_view(location)
		location = By.XPATH, "//a[text()='热点要闻']"
		page.scroll_into_view(location)

	def test_click_js(self,page):
		locator = By.ID, "s_btn_wr"
		current_url = page.driver.current_url
		page.click(locator)
		page.wait().until(page.EC.url_changes(current_url))
		assert page.driver.current_url == "https://www.baidu.com/?tn=news"
