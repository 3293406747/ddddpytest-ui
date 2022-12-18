import pytest
from selenium.webdriver.common.by import By
from pathlib import Path


class TestAlert:

	@pytest.fixture(scope="class", autouse=True)
	def goto(self, page):
		url = "file:///" + str(Path(__file__).resolve().parent / "data" / "alert.html")
		page.get(url)

	def test_alert(self, page):
		location = By.ID, "alert"
		page.click(location)
		alertText = page.switch_to_alert()
		assert alertText == "请点击确定按钮"

	def test_confirm(self, page):
		location = By.ID, "confirm"
		page.click(location)
		alertText = page.switch_to_alert()
		assert alertText == "请做出你的选择"

	def test_prompt(self, page):
		location = By.ID, "prompt"
		page.click(location)
		alertText = page.switch_to_alert()
		assert alertText == "请输入你的名字"

	def test_prompt_write(self, page):
		location = By.ID, "prompt"
		page.click(location)
		alertText = page.switch_to_alert(scanner="selenium")
		assert alertText == "请输入你的名字"