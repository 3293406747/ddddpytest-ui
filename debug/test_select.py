import pytest
from selenium.webdriver.common.by import By
from pathlib import Path


class TestSelect:

	@pytest.fixture(scope="class", autouse=True)
	def goto(self, page):
		url = "file:///" + str(Path(__file__).resolve().parent / "data" / "select.html")
		page.get(url)

	def test_select_index(self, page):
		locator = By.ID, "language"
		element = page.find_element(*locator)
		element.select(1,"index")
		assert element.get_attribute("value") == "1"

	def test_select_value(self, page):
		locator = By.ID, "language"
		element = page.find_element(*locator)
		element.select("2","value")
		assert element.get_attribute("value") == "2"

	def test_select_text(self, page):
		locator = By.ID, "language"
		element = page.find_element(*locator)
		element.select("javascript","text")
		assert element.get_attribute("value") == "3"