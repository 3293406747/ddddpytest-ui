from selenium import webdriver
import pytest
from base.basepage import BaseWebDriver



@pytest.fixture(scope="package", autouse=True)
def page():
	driver = webdriver.Firefox()
	page = BaseWebDriver(driver)
	page.maximize_window()
	yield page
	page.quit()