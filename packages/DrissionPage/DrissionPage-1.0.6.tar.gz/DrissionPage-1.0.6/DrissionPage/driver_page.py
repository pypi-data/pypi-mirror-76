# -*- coding:utf-8 -*-
"""
@Author  :   g1879
@Contact :   g1879@qq.com
@File    :   driver_page.py
"""
import time
from glob import glob
from typing import Union, List, Any
from urllib.parse import quote

from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from .common import get_loc_from_str, avoid_duplicate_name
from .driver_element import DriverElement, execute_driver_find


class DriverPage(object):
    """DriverPage封装了页面操作的常用功能，使用selenium来获取、解析、操作网页"""

    def __init__(self, driver: WebDriver, timeout: float = 10):
        """初始化函数，接收一个WebDriver对象，用来操作网页"""
        self._driver = driver
        self.timeout = timeout
        self._url = None
        self._url_available = None

    @property
    def driver(self) -> WebDriver:
        return self._driver

    @property
    def url(self) -> Union[str, None]:
        """当前网页url"""
        if not self._driver or not self.driver.current_url.startswith('http'):
            return None
        else:
            return self.driver.current_url

    @property
    def html(self) -> str:
        """获取元素innerHTML，如未指定元素则获取页面源代码"""
        return self.driver.find_element_by_xpath("//*").get_attribute("outerHTML")

    @property
    def url_available(self) -> bool:
        """url有效性"""
        return self._url_available

    @property
    def cookies(self) -> list:
        """返回当前网站cookies"""
        return self.driver.get_cookies()

    @property
    def title(self) -> str:
        """获取网页title"""
        return self.driver.title

    def get(self, url: str, go_anyway: bool = False) -> Union[None, bool]:
        """跳转到url"""
        to_url = quote(url, safe='/:&?=%;#@')
        if not url or (not go_anyway and self.url == to_url):
            return
        self._url = to_url
        self.driver.get(to_url)
        self._url_available = self.check_page()
        return self._url_available

    def ele(self,
            loc_or_ele: Union[tuple, str, DriverElement],
            mode: str = None,
            timeout: float = None,
            show_errmsg: bool = False) -> Union[DriverElement, List[DriverElement], None]:
        """根据loc获取元素或列表，可用字符串控制获取方式，可选'@属性名:'、'tag:'、'text:'、'css:'、'xpath:'
        如没有控制关键字，会按字符串文本搜索
        例：page.ele('@id:ele_id')，page.ele('首页')
        :param loc_or_ele: 页面元素地址
        :param mode: 以某种方式查找元素，可选'single' , 'all', 'visible'
        :param timeout: 是否显示错误信息
        :param show_errmsg: 是否显示错误信息
        :return: 页面元素对象或列表
        """
        if isinstance(loc_or_ele, DriverElement):
            return loc_or_ele
        elif isinstance(loc_or_ele, str):
            loc_or_ele = get_loc_from_str(loc_or_ele)

        timeout = timeout or self.timeout
        return execute_driver_find(self.driver, loc_or_ele, mode, show_errmsg, timeout)

    def eles(self, loc: Union[tuple, str], timeout: float = None, show_errmsg=False) -> List[DriverElement]:
        """查找符合条件的所有元素"""
        return self.ele(loc, mode='all', timeout=timeout, show_errmsg=show_errmsg)

    # ----------------以下为独有函数-----------------------
    def wait_ele(self,
                 loc_or_ele: Union[str, tuple, DriverElement, WebElement],
                 mode: str,
                 timeout: float = None) -> bool:
        """等待元素从dom删除、显示、隐藏
        :param loc_or_ele: 元素、获取元素的字符串或元素的loc
        :param mode: 等待方式，可选：'del', 'display', 'hidden'
        :param timeout: 超时时间
        :return: 等待是否成功
        """
        if mode.lower() not in ['del', 'display', 'hidden']:
            raise ValueError('Argument mode can only be "del", "display", "hidden"')

        from selenium.webdriver.support.wait import WebDriverWait
        from selenium.webdriver.support import expected_conditions as ec

        timeout = timeout or self.timeout
        is_ele = False
        if isinstance(loc_or_ele, DriverElement):
            loc_or_ele = loc_or_ele.inner_ele
            is_ele = True
        elif isinstance(loc_or_ele, WebElement):
            is_ele = True
        elif isinstance(loc_or_ele, str):
            loc_or_ele = get_loc_from_str(loc_or_ele)
        elif isinstance(loc_or_ele, tuple):
            pass
        else:
            raise TypeError('The type of loc_or_ele can only be str, tuple, DriverElement, WebElement')

        if is_ele:  # 当传入参数是元素对象时
            end_time = time.time() + timeout
            while time.time() < end_time:
                if mode == 'del':
                    try:
                        loc_or_ele.is_enabled()
                    except:
                        return True
                elif mode == 'display' and loc_or_ele.is_displayed():
                    return True
                elif mode == 'hidden' and not loc_or_ele.is_displayed():
                    return True
            return False
        else:  # 当传入参数是控制字符串或元组时
            try:
                if mode == 'del':
                    WebDriverWait(self.driver, timeout).until_not(ec.presence_of_element_located(loc_or_ele))
                elif mode == 'display':
                    WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located(loc_or_ele))
                elif mode == 'hidden':
                    WebDriverWait(self.driver, timeout).until_not(ec.visibility_of_element_located(loc_or_ele))
                return True
            except:
                return False

    def check_page(self) -> Union[bool, None]:
        """检查页面是否符合预期
        由子类自行实现各页面的判定规则"""
        return None

    def run_script(self, script: str) -> Any:
        """执行js脚本"""
        return self.driver.execute_script(script)

    def get_tabs_sum(self) -> int:
        """获取标签页数量"""
        return len(self.driver.window_handles)

    def get_tab_num(self) -> int:
        """获取当前tab号码"""
        handle = self.driver.current_window_handle
        handle_list = self.driver.window_handles
        return handle_list.index(handle)

    def create_tab(self):
        """新建并定位到一个标签页,该标签页在最后面"""
        self.to_tab(-1)
        self.run_script('window.open("");')
        self.to_tab(-1)

    def close_current_tab(self) -> None:
        """关闭当前标签页"""
        self.driver.close()

    def close_other_tabs(self, index: int = None) -> None:
        """传入序号，关闭序号以外标签页，没有传入序号代表保留当前页"""
        tabs = self.driver.window_handles  # 获得所有标签页权柄
        page_handle = tabs[index] if index >= 0 else self.driver.current_window_handle
        for i in tabs:  # 遍历所有标签页，关闭非保留的
            if i != page_handle:
                self.driver.switch_to.window(i)
                self.close_current_tab()
        self.driver.switch_to.window(page_handle)  # 把权柄定位回保留的页面

    def to_tab(self, index: int = 0) -> None:
        """跳转到第几个标签页，从0开始算"""
        tabs = self.driver.window_handles  # 获得所有标签页权柄
        self.driver.switch_to.window(tabs[index])

    def to_iframe(self, loc_or_ele: Union[int, str, tuple, WebElement, DriverElement] = 'main') -> None:
        """跳转到iframe
        :param loc_or_ele: 可接收iframe序号(0开始)、id或name、控制字符串、loc tuple、WebElement对象、DriverElement对象，
                            传入'main'跳到最高层，传入'parent'跳到上一层
        :return: None
        """
        if isinstance(loc_or_ele, int):
            # 根据序号跳转
            self.driver.switch_to.frame(loc_or_ele)
        elif isinstance(loc_or_ele, str):
            if loc_or_ele == 'main':  # 跳转到最上级
                self.driver.switch_to.default_content()
            elif loc_or_ele == 'parent':  # 跳转到上一层
                self.driver.switch_to.parent_frame()
            elif ':' not in loc_or_ele and '=' not in loc_or_ele:  # 传入id或name
                self.driver.switch_to.frame(loc_or_ele)
            else:  # 传入控制字符串
                ele = self.ele(loc_or_ele)
                self.driver.switch_to.frame(ele.inner_ele)
        elif isinstance(loc_or_ele, WebElement):
            self.driver.switch_to.frame(loc_or_ele)
        elif isinstance(loc_or_ele, DriverElement):
            self.driver.switch_to.frame(loc_or_ele.inner_ele)
        elif isinstance(loc_or_ele, tuple):
            ele = self.ele(loc_or_ele)
            self.driver.switch_to.frame(ele.inner_ele)

    def screenshot(self, path: str, filename: str = None) -> str:
        """获取网页截图"""
        name = filename or self.title
        name = avoid_duplicate_name(path, f'{name}.png')
        img_path = f'{path}\\{name}'
        self.driver.save_screenshot(img_path)
        # TODO: 实现全页截图
        return name

    def scroll_to_see(self, loc_or_ele: Union[str, tuple, WebElement, DriverElement]) -> None:
        """滚动直到元素可见"""
        ele = self.ele(loc_or_ele)
        ele.run_script("arguments[0].scrollIntoView();")

    def scroll_to(self, mode: str = 'bottom', pixel: int = 300) -> None:
        """滚动页面，按照参数决定如何滚动
        :param mode: 滚动的方向，top、bottom、rightmost、leftmost、up、down、left、right
        :param pixel: 滚动的像素
        :return: None
        """
        if mode == 'top':
            self.driver.execute_script("window.scrollTo(document.documentElement.scrollLeft,0);")
        elif mode == 'bottom':
            self.driver.execute_script(
                "window.scrollTo(document.documentElement.scrollLeft,document.body.scrollHeight);")
        elif mode == 'rightmost':
            self.driver.execute_script("window.scrollTo(document.body.scrollWidth,document.documentElement.scrollTop);")
        elif mode == 'leftmost':
            self.driver.execute_script("window.scrollTo(0,document.documentElement.scrollTop);")
        elif mode == 'up':
            self.driver.execute_script(f"window.scrollBy(0,-{pixel});")
        elif mode == 'down':
            self.driver.execute_script(f"window.scrollBy(0,{pixel});")
        elif mode == 'left':
            self.driver.execute_script(f"window.scrollBy(-{pixel},0);")
        elif mode == 'right':
            self.driver.execute_script(f"window.scrollBy({pixel},0);")
        else:
            raise ValueError(
                "Argument mode can only be 'top', 'bottom', 'rightmost', 'leftmost', 'up', 'down', 'left', 'right'.")

    def refresh(self) -> None:
        """刷新页面"""
        self.driver.refresh()

    def back(self) -> None:
        """后退"""
        self.driver.back()

    def set_window_size(self, x: int = None, y: int = None) -> None:
        """设置窗口大小，默认最大化"""
        if not x and not y:
            self.driver.maximize_window()
        else:
            if x <= 0 or y <= 0:
                raise ValueError('Arguments x and y must greater than 0.')
            new_x = x or self.driver.get_window_size()['width']
            new_y = y or self.driver.get_window_size()['height']
            self.driver.set_window_size(new_x, new_y)

    def chrome_downloading(self, download_path: str) -> list:
        """检查下载情况"""
        return glob(f'{download_path}\\*.crdownload')

    def process_alert(self, mode: str = 'ok', text: str = None) -> Union[str, None]:
        """处理提示框
        :param mode: 'ok' 或 'cancel'，若输入其它值，不会按按钮但依然返回文本值
        :param text: 处理prompt提示框时可输入文本
        :return:
        """
        try:
            alert = self.driver.switch_to.alert
        except NoAlertPresentException:
            return None
        if text:
            alert.send_keys(text)
        text = alert.text
        if mode == 'cancel':
            alert.dismiss()
        elif mode == 'ok':
            alert.accept()
        return text
