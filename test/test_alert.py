import time
import pytest
from selenium.webdriver.common.by import By
from pathlib import Path


class TestBaidu:

	@pytest.fixture(scope="class", autouse=True)
	def goto(self, page):
		url = "file:///" + str(Path(__file__).resolve().parent / "data" / "alert.html")
		page.get(url)

	def test_alert(self, page):
		location = By.ID, "alert"
		page.click(location)
		page.switch_to_alert()

	def test_confirm(self, page):
		location = By.ID, "confirm"
		page.click(location)
		page.switch_to_alert()

	def test_prompt(self, page):
		location = By.ID, "prompt"
		page.click(location)
		page.switch_to_alert()

	def test_prompt_write(self, page):
		location = By.ID, "prompt"
		page.click(location)
		page.switch_to_alert(scanner="selenium")
		time.sleep(5)