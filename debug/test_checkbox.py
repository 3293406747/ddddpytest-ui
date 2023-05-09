import pytest
from pathlib import Path


class TestCheckbox:

	@pytest.fixture(scope="class", autouse=True)
	def goto(self, page):
		url = "file:///" + str(Path(__file__).resolve().parent / "data" / "checkbox.html")
		page.get(url)

	def test_checkbox(self, page):
		value1 = "//span[@id='language']/label[1]/input"
		element1 = page.find_element(value=value1)
		element1.check_checkbox()
		value2 = "//span[@id='language']/label[2]/input"
		element2 = page.find_element(value=value2)
		element2.check_checkbox()
		value3 = "//span[@id='sex']/label[1]/input"
		element3 = page.find_element(value=value3)
		element3.check_checkbox()

	def test_uncheckbox(self,page):
		value1 = "//span[@id='language']/label[1]/input"
		element1 = page.find_element(value=value1)
		element1.uncheck_checkbox()
		value2 = "//span[@id='language']/label[2]/input"
		element2 = page.find_element(value=value2)
		element2.uncheck_checkbox()