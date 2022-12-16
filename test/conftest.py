from selenium import webdriver
import pytest
from base.basepage import BasePage



@pytest.fixture(scope="package", autouse=True)
def page():
	driver = webdriver.Chrome()
	basepage = BasePage(driver)
	basepage.maximize_window()
	yield basepage
	basepage.quit()