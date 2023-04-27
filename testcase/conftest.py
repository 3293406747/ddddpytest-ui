import time

import pytest
from selenium import webdriver
from base.basepage import BaseWebDriver
from utils.logger import logger


@pytest.fixture(scope="package",autouse=True)
def driver():
	driver = webdriver.Firefox()
	page = BaseWebDriver(driver)
	page.maximize_window()
	yield driver
	page.quit()



@pytest.fixture(autouse=True)
def performtime():
	start_time = time.time()
	logger.info(f"{'测试用例开始执行':*^60s}")
	yield
	logger.info(f"{'测试用例执行结束':*^60s}")
	end_time = time.time()
	logger.info(f"测试用例执行耗时：{end_time - start_time:.3f}秒")



