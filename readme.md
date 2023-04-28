:link:[真希望你没见过什么世面，一生只爱我这张平凡的脸](https://music.163.com/#/song?id=1963720173)

# 带带弟弟pytest-ui

本项目实现UI自动化的技术选型：**Python+Selenium+Pytest+Allure+Excel+Loguru** ，
通过Python+Selenium来操作浏览器， 使用Pytest作为测试执行器，
使用Allure生成测试报告，使用Excel管理测试数据，使用Loguru管理日志。

## 特征

- 采用pom(page object module)设计模式,将元素处理与业务分离
- 项目运行自动生成错误截图、Log日志文件、Allure报告
- 支持多套配置文件之间切换
- 支持mysql数据库连接及操作

:loudspeaker:项目测试环境：win11+python3.10

## Demo部署

- 下载项目源码后，在根目录下找到**requirements.txt**文件，然后通过 pip 工具安装 requirements.txt 依赖，执行命令：

```shell
pip3 install -r requirements.txt
```
- 下载浏览器对应版本的驱动并放到项目目录下，下载安装教程如下: https://www.cnblogs.com/123polaris/p/16435523.html
```text
常用浏览器驱动下载地址:
Chrome: https://registry.npmmirror.com/binary.html?path=chromedriver
Firfox: https://github.com/mozilla/geckodriver/releases
Ie: http://selenium-release.storage.googleapis.com/index.html
```
- 下载并配置allure2，下载安装教程如下：https://blog.csdn.net/lixiaomei0623/article/details/120185069

- 之后运行**main.py**，或在Terminal窗口cd到项目根目录后执行命令：

```shell
pytest
```

## demo

```python
""" testcase/test_baidu.py """
import pytest
from utils.read_excel import read_excel
from page.baidu import BaiduPage
from testcase import BASE_PATH


class TestBaidu:

	@pytest.mark.parametrize("case", read_excel(str(BASE_PATH.joinpath("baidu.xlsx"))))
	def test_select(self, case, driver):
		page_baidu = BaiduPage(driver)
		page_baidu.get(page_baidu.url)
		page_baidu.select(case["scanner"])
```

```python
""" page/baidu.py """
from selenium.webdriver.common.by import By
from base.basepage import BaseWebDriver


class BaiduPage(BaseWebDriver):
	""" 百度首页 """
	url = "https://www.baidu.com"
	
	kw = By.ID, "kw"
	su = By.ID, "su"

	def select(self, content):
		""" 百度搜索 """
		element_input = self.find_element(*self.kw,name="百度输入框")
		element_input.write(content)
		
		element_button = self.find_element(*self.su,name="百度一下按钮")
		element_button.click()
```

## 支持

1. 如果喜欢ddddpytest-ui，可以在GitHub Star。
2. 本项目使用过程中遇到问题或一起交流学习可添加微信或
[telegram](https://t.me/qingtest) 进行沟通。

![vx](img/vx.jpg)