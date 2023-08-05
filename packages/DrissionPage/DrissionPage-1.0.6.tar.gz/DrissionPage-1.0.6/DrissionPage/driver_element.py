# -*- coding:utf-8 -*-
"""
@Author  :   g1879
@Contact :   g1879@qq.com
@File    :   driver_element.py
"""
from html import unescape
from pathlib import Path
from time import sleep
from typing import Union, List, Any

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from .common import DrissionElement, get_loc_from_str, translate_loc_to_xpath, avoid_duplicate_name


class DriverElement(DrissionElement):
    """driver模式的元素对象，包装了一个WebElement对象，并封装了常用功能"""

    def __init__(self, ele: WebElement, timeout: float = 10):
        super().__init__(ele)
        self.timeout = timeout
        self._driver = ele.parent

    def __repr__(self):
        attrs = [f"{attr}='{self.attrs[attr]}'" for attr in self.attrs]
        return f'<DriverElement {self.tag} {" ".join(attrs)}>'

    @property
    def driver(self) -> WebDriver:
        return self._driver

    @property
    def attrs(self) -> dict:
        """返回元素所有属性及值"""
        js = '''
        var dom=arguments[0];
        var names="(";
        var len = dom.attributes.length;
        for(var i=0;i<len;i++){
            let it = dom.attributes[i];
            let localName = it.localName;
            //let value = it.value;
            //names += "'" + localName + "':'" + value.replace(/'/g,"\\\\'") + "', ";  
            names += "'" + localName + "',";  
        }
        names+=")"
        return names;  
        '''
        attrs = dict()
        for attr in eval(self.run_script(js)):
            attrs[attr] = self.attr(attr)
        return attrs

    @property
    def text(self) -> str:
        """元素内文本"""
        return unescape(self.attr('innerText')).replace('\xa0', ' ')

    @property
    def html(self) -> str:
        """元素innerHTML"""
        return unescape(self.attr('innerHTML')).replace('\xa0', ' ')

    @property
    def tag(self) -> str:
        """元素类型"""
        return self._inner_ele.tag_name

    @property
    def parent(self):
        """父级元素"""
        return self.parents()

    @property
    def next(self):
        """下一个兄弟元素"""
        return self.nexts()

    @property
    def prev(self):
        """上一个兄弟元素"""
        return self.prevs()

    def parents(self, num: int = 1):
        """N层父级元素"""
        loc = 'xpath', f'.{"/.." * num}'
        return self.ele(loc, timeout=1, show_errmsg=False)

    def nexts(self, num: int = 1):
        """下N个兄弟元素"""
        loc = 'xpath', f'./following-sibling::*[{num}]'
        return self.ele(loc, timeout=1, show_errmsg=False)

    def prevs(self, num: int = 1):
        """上N个兄弟元素"""
        loc = 'xpath', f'./preceding-sibling::*[{num}]'
        return self.ele(loc, timeout=1, show_errmsg=False)

    def attr(self, attr: str) -> str:
        """获取属性值"""
        if attr == 'text':
            return self.text
        else:
            # return self.attrs[attr]
            return self.inner_ele.get_attribute(attr)

    def ele(self,
            loc_or_str: Union[tuple, str],
            mode: str = None,
            show_errmsg: bool = False,
            timeout: float = None):
        """根据loc获取元素或列表，可用字符串控制获取方式，可选'@属性名:'、'tag:'、'text:'、'css:'、'xpath:'
        如没有控制关键字，会按字符串文本搜索
        例：ele.ele('@id:ele_id')，ele.ele('首页')
        """
        if isinstance(loc_or_str, str):
            loc_or_str = get_loc_from_str(loc_or_str)
        elif isinstance(loc_or_str, tuple) and len(loc_or_str) == 2:
            loc_or_str = translate_loc_to_xpath(loc_or_str)
        else:
            raise ValueError('Argument loc_or_str can only be tuple or str.')

        if loc_or_str[0] == 'xpath':
            # 确保查询语句最前面是.
            loc_str = f'.{loc_or_str[1]}' if not loc_or_str[1].startswith('.') else loc_or_str[1]
            loc_or_str = loc_or_str[0], loc_str

        timeout = timeout or self.timeout
        return execute_driver_find(self.inner_ele, loc_or_str, mode, show_errmsg, timeout)

    def eles(self,
             loc_or_str: Union[tuple, str],
             show_errmsg: bool = False,
             timeout: float = None):
        """根据loc获取子元素列表"""
        return self.ele(loc_or_str, mode='all', show_errmsg=show_errmsg, timeout=timeout)

    # -----------------以下为driver独占-------------------
    def click(self, by_js=None) -> bool:
        """点击"""
        if not by_js:
            for _ in range(10):
                try:
                    self.inner_ele.click()
                    return True
                except:
                    sleep(0.2)
        # 若点击失败，用js方式点击
        if by_js is not False:
            self.run_script('arguments[0].click()')
            return True
        return False

    def input(self, value, clear: bool = True) -> bool:
        """输入文本"""
        try:
            if clear:
                self.clear()
            self.inner_ele.send_keys(value)
            return True
        except Exception as e:
            print(e)
            return False

    def run_script(self, script: str) -> Any:
        """运行js"""
        return self.inner_ele.parent.execute_script(script, self.inner_ele)

    def submit(self) -> None:
        """提交表单"""
        self.inner_ele.submit()

    def clear(self) -> None:
        """清空元素"""
        self.run_script("arguments[0].value=''")
        # self.ele.clear()

    def is_selected(self) -> bool:
        """是否选中"""
        return self.inner_ele.is_selected()

    def is_enabled(self) -> bool:
        """是否可用"""
        return self.inner_ele.is_enabled()

    def is_displayed(self) -> bool:
        """是否可见"""
        return self.inner_ele.is_displayed()

    def is_valid(self) -> bool:
        """用于判断元素是否还能用，应对页面跳转元素不能用的情况"""
        try:
            self.is_enabled()
            return True
        except:
            return False

    @property
    def size(self) -> dict:
        """元素大小"""
        return self.inner_ele.size

    @property
    def location(self) -> dict:
        """元素坐标"""
        return self.inner_ele.location

    def screenshot(self, path: str, filename: str = None) -> str:
        """元素截图"""
        name = filename or self.tag
        name = avoid_duplicate_name(path, f'{name}.png')
        Path(path).mkdir(parents=True, exist_ok=True)
        # 等待元素加载完成
        if self.tag == 'img':
            js = 'return arguments[0].complete && typeof arguments[0].naturalWidth != "undefined" ' \
                 '&& arguments[0].naturalWidth > 0'
            while not self.run_script(js):
                pass
        img_path = f'{path}\\{name}'
        self.inner_ele.screenshot(img_path)
        return img_path

    def select(self, text: str) -> bool:
        """在下拉列表中选择"""
        ele = Select(self.inner_ele)
        try:
            ele.select_by_visible_text(text)
            return True
        except:
            return False

    def set_attr(self, attr: str, value: str) -> bool:
        """设置元素属性"""
        try:
            self.run_script(f"arguments[0].{attr} = '{value}';")
            return True
        except Exception as e:
            print(e)
            return False

    def drag(self, x: int, y: int, speed: int = 40, shake: bool = True) -> bool:
        """拖拽当前元素到相对位置
        :param x: x变化值
        :param y: y变化值
        :param speed: 速度
        :param shake: 是否随机抖动
        :return: 是否推拽成功
        """
        x += self.location['x'] + self.size['width'] // 2
        y += self.location['y'] + self.size['height'] // 2
        return self.drag_to((x, y), speed, shake)

    def drag_to(self,
                ele_or_loc: Union[tuple, WebElement, DrissionElement],
                speed: int = 40,
                shake: bool = True) -> bool:
        """拖拽当前元素，目标为另一个元素或坐标元组
        :param ele_or_loc: 另一个元素或坐标元组，坐标为元素中点的坐标
        :param speed: 拖动的速度，默认为None即瞬间到达
        :param shake: 是否随机抖动
        :return: 是否拖拽成功
        """
        # x, y：目标坐标点
        if isinstance(ele_or_loc, DriverElement) or isinstance(ele_or_loc, WebElement):
            target_x = ele_or_loc.location['x'] + ele_or_loc.size['width'] // 2
            target_y = ele_or_loc.location['y'] + ele_or_loc.size['height'] // 2
        elif isinstance(ele_or_loc, tuple):
            target_x, target_y = ele_or_loc
        else:
            raise TypeError('Need DriverElement, WebElement object or coordinate information.')

        current_x = self.location['x'] + self.size['width'] // 2
        current_y = self.location['y'] + self.size['height'] // 2
        width = target_x - current_x
        height = target_y - current_y
        num = 0 if not speed else int(((abs(width) ** 2 + abs(height) ** 2) ** .5) // speed)
        # 将要经过的点存入列表
        points = [(int(current_x + i * (width / num)), int(current_y + i * (height / num))) for i in range(1, num)]
        points.append((target_x, target_y))

        from selenium.webdriver import ActionChains
        from random import randint
        actions = ActionChains(self.driver)
        actions.click_and_hold(self.inner_ele)
        loc1 = self.location
        for x, y in points:  # 逐个访问要经过的点
            if shake:
                x += randint(-3, 4)
                y += randint(-3, 4)
            actions.move_by_offset(x - current_x, y - current_y)
            current_x, current_y = x, y
        actions.release().perform()

        return False if self.location == loc1 else True

    def hover(self):
        """鼠标悬停"""
        from selenium.webdriver import ActionChains
        ActionChains(self._driver).move_to_element(self.inner_ele).perform()


def execute_driver_find(page_or_ele: Union[WebElement, WebDriver],
                        loc: tuple,
                        mode: str = 'single',
                        show_errmsg: bool = False,
                        timeout: float = 10) -> Union[DriverElement, List[DriverElement]]:
    """执行driver模式元素的查找
    页面查找元素及元素查找下级元素皆使用此方法
    :param page_or_ele: driver模式页面或元素
    :param loc: 元素定位语句
    :param mode: 'single'或'all'
    :param show_errmsg: 是否显示错误信息
    :param timeout: 查找元素超时时间
    :return: 返回DriverElement元素或列表
    """
    mode = mode or 'single'
    if mode not in ['single', 'all']:
        raise ValueError("Argument mode can only be 'single' or 'all'.")
    msg = result = None
    try:
        wait = WebDriverWait(page_or_ele, timeout=timeout)
        if mode == 'single':
            msg = 'Element not found.'
            result = DriverElement(wait.until(ec.presence_of_element_located(loc)))
        elif mode == 'all':
            msg = 'Elements not found.'
            eles = wait.until(ec.presence_of_all_elements_located(loc))
            result = [DriverElement(ele) for ele in eles]
        return result
    except:
        if show_errmsg:
            print(msg, loc)
            raise
        return [] if mode == 'all' else None
