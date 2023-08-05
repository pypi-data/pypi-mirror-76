# -*- coding:utf-8 -*-
"""
@Author  :   g1879
@Contact :   g1879@qq.com
@File    :   session_page.py
"""
import os
import re
from pathlib import Path
from random import randint
from time import time
from typing import Union, List
from urllib.parse import urlparse, quote

from requests_html import HTMLSession, HTMLResponse

from .common import get_loc_from_str, translate_loc_to_xpath, avoid_duplicate_name
from .config import OptionsManager
from .session_element import SessionElement, execute_session_find


class SessionPage(object):
    """SessionPage封装了页面操作的常用功能，使用requests_html来获取、解析网页。"""

    def __init__(self, session: HTMLSession, timeout: float = 10):
        """初始化函数"""
        self._session = session
        self.timeout = timeout
        self._url = None
        self._url_available = None
        self._response = None

    @property
    def session(self) -> HTMLSession:
        return self._session

    @property
    def response(self) -> HTMLResponse:
        return self._response

    @property
    def url(self) -> str:
        """当前访问url"""
        return self._url

    @property
    def url_available(self) -> bool:
        """url有效性"""
        return self._url_available

    @property
    def cookies(self) -> dict:
        """当前session的cookies"""
        return self.session.cookies.get_dict()

    @property
    def title(self) -> str:
        """获取网页title"""
        return self.ele(('css selector', 'title')).text

    @property
    def html(self) -> str:
        """获取元素innerHTML，如未指定元素则获取所有源代码"""
        return self.response.html.html

    def ele(self,
            loc_or_ele: Union[tuple, str, SessionElement],
            mode: str = None,
            show_errmsg: bool = False) -> Union[SessionElement, List[SessionElement], None]:
        """根据loc获取元素或列表，可用字符串控制获取方式，可选'@属性名:'、'tag:'、'text:'、'css:'、'xpath:'
        如没有控制关键字，会按字符串文本搜索
        例：page.ele('@id:ele_id')，page.ele('首页')
        :param loc_or_ele: 页面元素地址
        :param mode: 以某种方式查找元素，可选'single','all'
        :param show_errmsg: 是否显示错误信息
        :return: 页面元素对象或列表
        """
        if isinstance(loc_or_ele, SessionElement):
            return loc_or_ele
        elif isinstance(loc_or_ele, str):
            loc = get_loc_from_str(loc_or_ele)
        else:
            loc = translate_loc_to_xpath(loc_or_ele)

        return execute_session_find(self.response.html, loc, mode, show_errmsg)

    def eles(self, loc: Union[tuple, str], show_errmsg: bool = False) -> List[SessionElement]:
        """查找符合条件的所有元素"""
        return self.ele(loc, mode='all', show_errmsg=True)

    def get(self, url: str, go_anyway: bool = False, **kwargs) -> Union[bool, None]:
        """用get方式跳转到url，调用_make_response()函数生成response对象"""
        to_url = quote(url, safe='/:&?=%;#@')
        if not url or (not go_anyway and self.url == to_url):
            return
        self._url = to_url
        self._response = self._make_response(to_url, **kwargs)[0]
        if self._response:
            self._response.html.encoding = self._response.encoding  # 修复requests_html丢失编码方式的bug
        self._url_available = True if self._response and self._response.ok else False
        return self._url_available

    def post(self, url: str, data: dict = None, go_anyway: bool = False, **kwargs) -> Union[bool, None]:
        """用post方式跳转到url，调用_make_response()函数生成response对象"""
        to_url = quote(url, safe='/:&?=%;#@')
        if not url or (not go_anyway and self._url == to_url):
            return
        self._url = to_url
        self._response = self._make_response(to_url, mode='post', data=data, **kwargs)[0]
        if self._response:
            try:
                self._response.html.encoding = self._response.encoding  # 修复requests_html丢失编码方式的bug
            except:
                pass
        self._url_available = True if self._response and self._response.status_code == 200 else False
        return self._url_available

    def download(self,
                 file_url: str,
                 goal_path: str = None,
                 rename: str = None,
                 file_exists: str = 'rename',
                 show_msg: bool = False,
                 **kwargs) -> tuple:
        """下载一个文件
        生成的response不写入self._response，是临时的
        :param file_url: 文件url
        :param goal_path: 存放路径url
        :param rename: 重命名文件，不改变扩展名
        :param kwargs: 连接参数
        :param file_exists: 若存在同名文件，可选择'rename', 'overwrite', 'skip'方式处理
        :param show_msg: 是否显示下载信息
        :return: 元组，bool和状态信息（成功时信息为文件路径）
        """
        goal_path = goal_path or OptionsManager().get_value('paths', 'global_tmp_path')
        if not goal_path:
            raise IOError('No path specified.')

        kwargs['stream'] = True
        if 'timeout' not in kwargs:
            kwargs['timeout'] = 20

        r, info = self._make_response(file_url, mode='get', **kwargs)
        if not r:
            if show_msg:
                print(info)
            return False, info
        # -------------------获取文件名-------------------
        # header里有文件名，则使用它，否则在url里截取，但不能保证url包含文件名
        if 'Content-disposition' in r.headers:
            file_name = r.headers['Content-disposition'].split('"')[1].encode('ISO-8859-1').decode('utf-8')
        elif os.path.basename(file_url):
            file_name = os.path.basename(file_url).split("?")[0]
        else:
            file_name = f'untitled_{time()}_{randint(0, 100)}'

        file_name = re.sub(r'[\\/*:|<>?"]', '', file_name).strip()
        if rename:  # 重命名文件，不改变扩展名
            rename = re.sub(r'[\\/*:|<>?"]', '', rename).strip()
            ext_name = file_name.split('.')[-1]
            if rename.lower().endswith(f'.{ext_name}'.lower()) or ext_name == file_name:
                full_name = rename
            else:
                full_name = f'{rename}.{ext_name}'
        else:
            full_name = file_name

        goal_Path = Path(goal_path)
        goal_path = ''
        for key, i in enumerate(goal_Path.parts):  # 去除路径中的非法字符
            goal_path += goal_Path.drive if key == 0 and goal_Path.drive else re.sub(r'[*:|<>?"]', '', i).strip()
            goal_path += '\\' if i != '\\' and key < len(goal_Path.parts) - 1 else ''

        goal_Path = Path(goal_path)
        goal_Path.mkdir(parents=True, exist_ok=True)
        goal_path = goal_Path.absolute()
        full_path = Path(f'{goal_path}\\{full_name}')

        if full_path.exists():
            if file_exists == 'skip':
                return False, 'A file with the same name already exists.'
            elif file_exists == 'overwrite':
                pass
            elif file_exists == 'rename':
                full_name = avoid_duplicate_name(goal_path, full_name)
                full_path = Path(f'{goal_path}\\{full_name}')
            else:
                raise ValueError("Argument file_exists can only be 'skip', 'overwrite', 'rename'.")

        if show_msg:  # 打印要下载的文件
            print(full_name if file_name == full_name else f'{file_name} -> {full_name}')
            print(f'Downloading to: {goal_path}')

        # -------------------开始下载-------------------
        # 获取远程文件大小
        file_size = int(r.headers['Content-Length']) if 'Content-Length' in r.headers else None
        downloaded_size, download_status = 0, False  # 已下载文件大小和下载状态
        try:
            with open(str(full_path), 'wb') as tmpFile:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        tmpFile.write(chunk)
                        if show_msg and file_size:  # 如表头有返回文件大小，显示进度
                            downloaded_size += 1024
                            rate = downloaded_size / file_size if downloaded_size < file_size else 1
                            print('\r {:.0%} '.format(rate), end="")
        except Exception as e:
            download_status, info = False, f'Download failed.\n{e}'
        else:
            download_status, info = (False, 'File size is 0.') if full_path.stat().st_size == 0 else (True, 'Success.')
        finally:
            # 删除下载出错文件
            if not download_status and full_path.exists():
                full_path.unlink()
            r.close()
        # -------------------显示并返回值-------------------
        if show_msg:
            print(info)
        info = f'{goal_path}\\{full_name}' if download_status else info
        return download_status, info

    def _make_response(self, url: str, mode: str = 'get', data: dict = None, **kwargs) -> tuple:
        """生成response对象。接收mode参数，以决定用什么方式。
        :param url: 要访问的网址
        :param mode: 'get', 'post' 中选择
        :param data: 提交的数据
        :param kwargs: 其它参数
        :return: Response对象
        """
        if mode not in ['get', 'post']:
            raise ValueError("Argument mode can only be 'get' or 'post'.")
        url = quote(url, safe='/:&?=%;#@')

        # 设置referer和host值
        kwargs_set = set(x.lower() for x in kwargs)
        if 'headers' in kwargs_set:
            header_set = set(x.lower() for x in kwargs['headers'])
            if self.url and 'referer' not in header_set:
                kwargs['headers']['Referer'] = self.url
            if 'host' not in header_set:
                kwargs['headers']['Host'] = urlparse(url).hostname
        else:
            kwargs['headers'] = self.session.headers
            kwargs['headers']['Host'] = urlparse(url).hostname
            if self.url:
                kwargs['headers']['Referer'] = self._url

        if 'timeout' not in kwargs_set:
            kwargs['timeout'] = self.timeout

        try:
            r = None
            if mode == 'get':
                r = self.session.get(url, **kwargs)
            elif mode == 'post':
                r = self.session.post(url, data=data, **kwargs)
        except Exception as e:
            return None, e
        else:
            headers = dict(r.headers)
            if 'Content-Type' not in headers or 'charset' not in headers['Content-Type']:
                re_result = re.search(r'<meta.*?charset=[ \'"]*([^"\' />]+).*?>', r.text)
                try:
                    charset = re_result.group(1)
                except:
                    charset = 'utf-8'
            else:
                charset = headers['Content-Type'].split('=')[1]
            # 避免存在退格符导致乱码或解析出错
            r._content = r.content if 'stream' in kwargs and kwargs['stream'] else r.content.replace(b'\x08', b'\\b')
            r.encoding = charset
            return r, 'Success'
