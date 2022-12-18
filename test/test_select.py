import pytest
from selenium.webdriver.common.by import By
from pathlib import Path


class TestSelect:

	@pytest.fixture(scope="class", autouse=True)
	def goto(self, page):
		url = "file:///" + str(Path(__file__).resolve().parent / "data" / "select.html")
		page.get(url)

	def test_select_index(self, page):
		location = By.ID, "language"
		page.select(location,1,"index")
		assert page.find_element(location).get_attribute("value") == "1"

	def test_select_value(self, page):
		location = By.ID, "language"
		page.select(location,"2","value")
		assert page.find_element(location).get_attribute("value") == "2"

	def test_select_text(self, page):
		location = By.ID, "language"
		page.select(location,"javascript","text")
		assert page.find_element(location).get_attribute("value") == "3"