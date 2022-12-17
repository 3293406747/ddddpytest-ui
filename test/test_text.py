import pytest
from selenium.webdriver.common.by import By


class TestBaidu:

	@pytest.fixture(scope="class", autouse=True)
	def goto(self, page):
		page.get("https://www.baidu.com")


	def test_text(self, page):
		location = By.CSS_SELECTOR, "span#s-usersetting-top"
		text = page.get_text(location)
		assert text == "设置"

	def test_texts(self, page):
		location = By.XPATH, "//div[@id='s-top-left']/a[text()]"
		texts = page.get_texts(location)
		assert isinstance(texts, list)
		assert texts == ["新闻", "hao123","地图","贴吧","视频","图片","网盘"]

	def test_attribute(self, page):
		location = By.ID, "su"
		text = page.get_attribute(location,"value")
		assert text == "百度一下"

	def test_attributes(self, page):
		location = By.XPATH, "//input[@value != '']"
		texts = page.get_attributes(location,"value")
		print(texts)
		assert isinstance(texts,list)