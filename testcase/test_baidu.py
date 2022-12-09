import pytest,allure
from common.read.read_excel import read_excel
from page.baidu import BaiduPage


@allure.epic("ddddpytest-ui web自动化测试项目")
@allure.feature("测试百度")
class TestBaidu:

	@pytest.fixture(scope="class",autouse=True)
	def page(self,driver):
		page = BaiduPage(driver)
		return page

	@allure.story("测试百度搜索")
	@pytest.mark.parametrize("case",read_excel("baidu.xlsx"))
	def test_select(self,case,page):
		allure.dynamic.title(case["用例名称"])
		page.get(page.url)
		page.baidu_select(case["input_text"])