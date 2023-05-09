import pytest
from selenium.webdriver.common.by import By
from pathlib import Path


class TestAlert:

	@pytest.fixture(scope="class", autouse=True)
	def goto(self, page):
		url = "file:///" + str(Path(__file__).resolve().parent / "data" / "alert.html")
		page.get(url)

	def test_alert(self, page):
		locator = By.ID, "alert"
		element = page.find_element(*locator)
		element.click()
		alert_text = page.switch_to_alert()
		assert alert_text == "请点击确定按钮"

	def test_confirm(self, page):
		locator = By.ID, "confirm"
		element = page.find_element(*locator)
		element.click()
		alert_text = page.switch_to_alert()
		assert alert_text == "请做出你的选择"

	def test_prompt(self, page):
		locator = By.ID, "prompt"
		element = page.find_element(*locator)
		element.click()
		alert_text = page.switch_to_alert()
		assert alert_text == "请输入你的名字"

	def test_prompt_write(self, page):
		locator = By.ID, "prompt"
		element = page.find_element(*locator)
		element.click()
		alert_text = page.switch_to_alert(scanner="selenium")
		assert alert_text == "请输入你的名字"