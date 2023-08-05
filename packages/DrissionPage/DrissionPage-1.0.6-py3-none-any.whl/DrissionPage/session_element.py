# -*- coding:utf-8 -*-
"""
@Author  :   g1879
@Contact :   g1879@qq.com
@File    :   session_element.py
"""
import re
from html import unescape
from typing import Union, List

from requests_html import Element, BaseParser

from .common import DrissionElement, get_loc_from_str, translate_loc_to_xpath


class SessionElement(DrissionElement):
    """session模式的元素对象，包装了一个Element对象，并封装了常用功能"""

    def __init__(self, ele: Element):
        super().__init__(ele)

    def __repr__(self):
        attrs = [f"{attr}='{self.attrs[attr]}'" for attr in self.attrs]
        return f'<SessionElement {self.tag} {" ".join(attrs)}>'

    @property
    def attrs(self) -> dict:
        """返回元素所有属性及值"""
        attrs = dict()
        for attr in self.inner_ele.attrs:
            attrs[attr] = self.attr(attr)
        return attrs

    @property
    def text(self) -> str:
        """元素内文本"""
        return unescape(self._inner_ele.text).replace('\xa0', ' ')

    @property
    def html(self) -> str:
        """元素innerHTML"""
        html = unescape(self._inner_ele.html).replace('\xa0', ' ')
        r = re.match(r'<.*?>(.*)</.*?>', html, flags=re.DOTALL)
        return None if not r else r.group(1)

    @property
    def tag(self) -> str:
        """获取标签名"""
        return self._inner_ele.tag

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
        """requests_html的Element打包了lxml的元素对象，从lxml元素对象读取上下级关系后再重新打包"""
        try:
            return SessionElement(
                Element(element=self.inner_ele.element.xpath(f'..{"/.." * (num - 1)}')[0], url=self.inner_ele.url))
        except IndexError:
            return None

    def nexts(self, num: int = 1):
        """requests_html的Element打包了lxml的元素对象，从lxml元素对象读取上下级关系后再重新打包"""
        try:
            return SessionElement(
                Element(element=self.inner_ele.element.xpath(f'./following-sibling::*[{num}]')[0],
                        url=self.inner_ele.url))
        except IndexError:
            return None

    def prevs(self, num: int = 1):
        """requests_html的Element打包了lxml的元素对象，从lxml元素对象读取上下级关系后再重新打包"""
        try:
            return SessionElement(
                Element(element=self.inner_ele.element.xpath(f'./preceding-sibling::*[{num}]')[0],
                        url=self.inner_ele.url))
        except IndexError:
            return None

    def ele(self, loc_or_str: Union[tuple, str], mode: str = None, show_errmsg: bool = False):
        """根据loc获取元素或列表，可用字符串控制获取方式，可选'@属性名:'、'tag:'、'text:'、'css:'、'xpath:'
        如没有控制关键字，会按字符串文本搜索
        例：ele.ele('@id:ele_id')，ele.ele('首页')
        """
        if isinstance(loc_or_str, str):
            loc_or_str = get_loc_from_str(loc_or_str)
        elif isinstance(loc_or_str, tuple) and len(loc_or_str) == 2:
            loc_or_str = translate_loc_to_xpath(loc_or_str)
        else:
            raise TypeError('Type of loc_or_str can only be tuple or str.')

        loc_str = None
        if loc_or_str[0] == 'xpath':
            # Element的html是包含自己的，要如下处理，使其只检索下级的
            loc_str = f'./{self.tag}{loc_or_str[1].lstrip(".")}'
        elif loc_or_str[0] == 'css selector':
            loc_str = f':root>{self.tag}{loc_or_str[1]}'
        loc_or_str = loc_or_str[0], loc_str

        return execute_session_find(self.inner_ele, loc_or_str, mode, show_errmsg)

    def eles(self, loc_or_str: Union[tuple, str], show_errmsg: bool = False):
        return self.ele(loc_or_str, mode='all', show_errmsg=show_errmsg)

    def attr(self, attr: str) -> str:
        """获取属性值"""
        try:
            if attr == 'href':
                # 如直接获取attr只能获取相对地址
                link = self._inner_ele.attrs['href']
                if link.lower().startswith(('javascript:', 'mailto:')):
                    return link
                elif link.startswith('#'):
                    if '#' in self.inner_ele.url:
                        return re.sub(r'#.*', link, self.inner_ele.url)
                    else:
                        return f'{self.inner_ele.url}{link}'
                elif link.startswith('?'):  # 避免当相对URL以?开头时requests-html丢失参数的bug
                    if '?' in self.inner_ele.url:
                        return re.sub(r'\?.*', link, self.inner_ele.url)
                    else:
                        return f'{self.inner_ele.url}{link}'
                else:
                    for link in self._inner_ele.absolute_links:
                        return link
            elif attr == 'src':
                return self._inner_ele._make_absolute(self._inner_ele.attrs['src'])
            elif attr == 'class':
                return ' '.join(self._inner_ele.attrs['class'])
            elif attr == 'text':
                return self.text
            else:
                return self._inner_ele.attrs[attr]
        except:
            return ''


def execute_session_find(page_or_ele: BaseParser,
                         loc: tuple,
                         mode: str = 'single',
                         show_errmsg: bool = False) -> Union[SessionElement, List[SessionElement]]:
    """执行session模式元素的查找
    页面查找元素及元素查找下级元素皆使用此方法
    :param page_or_ele: session模式页面或元素
    :param loc: 元素定位语句
    :param mode: 'single'或'all'
    :param show_errmsg: 是否显示错误信息
    :return: 返回SessionElement元素或列表
    """
    mode = mode or 'single'
    if mode not in ['single', 'all']:
        raise ValueError("Argument mode can only be 'single' or 'all'.")
    loc_by, loc_str = loc
    msg = result = first = None
    try:
        if mode == 'single':
            msg = 'Element not found.'
            first = True
        elif mode == 'all':
            msg = 'Elements not found.'
            first = False

        if loc_by == 'xpath':
            ele = page_or_ele.xpath(loc_str, first=first)
        else:
            ele = page_or_ele.find(loc_str, first=first)

        if mode == 'single':
            result = SessionElement(ele) if ele else None
        elif mode == 'all':
            result = [SessionElement(e) for e in ele]

        return result
    except:
        if show_errmsg:
            print(msg, loc)
            raise
        return [] if mode == 'all' else None
