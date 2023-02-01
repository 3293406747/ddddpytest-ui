import pytest
from selenium.webdriver.common.by import By
from pathlib import Path


class TestCheckbox:

	@pytest.fixture(scope="class", autouse=True)
	def goto(self, page):
		url = "file:///" + str(Path(__file__).resolve().parent / "data" / "checkbox.html")
		page.get(url)

	def test_checkbox(self, page):
		location1 = By.XPATH, "//span[@id='language']/label[1]/input"
		page.check_checkbox(location1)
		location2 = By.XPATH, "//span[@id='language']/label[2]/input"
		page.check_checkbox(location2)
		location3 = By.XPATH, "//span[@id='sex']/label[1]/input"
		page.check_checkbox(location3)

	def test_uncheckbox(self,page):
		location1 = By.XPATH, "//span[@id='language']/label[1]/input"
		page.uncheck_checkbox(location1)
		location2 = By.XPATH, "//span[@id='language']/label[2]/input"
		page.uncheck_checkbox(location2)