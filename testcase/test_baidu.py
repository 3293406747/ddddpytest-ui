import pytest, allure
from utils.readExcel import readExcel
from page.baidu import BaiduPage
from testcase import BASEPATH


@allure.epic("ddddpytest-ui web自动化测试项目")
@allure.feature("测试百度")
class TestBaidu:

	@allure.story("测试百度搜索")
	@pytest.mark.parametrize("case", readExcel(str(BASEPATH / "baidu.xlsx")))
	def test_select(self, case, driver):
		allure.dynamic.title(case["用例名称"])
		page_baidu = BaiduPage(driver)
		page_baidu.get(page_baidu.url)
		page_baidu.select(case["scanner"])
