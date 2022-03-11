# -*- coding: utf-8 -*-
import httpx
import asyncio
import time
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup
from .config import UrlConfig
from .encrypt import encrypt


class Auth(object):
    """南农门户验证类

    该类主要内容是南农办事大厅登入登出、验证码查询接口的实现。

    Attributes:
        _account: 登入账号（学号）
        _password: 账号密钥
    """

    def __init__(self, account, password, **kwargs):
        self._account = account
        self._password = password
        self._current = int(time.time() * 1000)
        self.client = httpx.Client(follow_redirects=True, timeout=kwargs.get('timeout', 5))

    def check_captcha(self) -> dict:
        """检查账号登录是否需要验证（isNeed）"""
        check_captcha_url = UrlConfig.portal_check_captcha_url + "?username=%s&_=%s" % (self._account, self._current)
        check_captcha_content = self.client.get(check_captcha_url)
        return check_captcha_content.json()

    def get_captcha(self) -> Image:
        """获取登录验证码"""
        captcha_url = UrlConfig.portal_captcha_url + "?%s" % self._current
        captcha_content = self.client.get(captcha_url)
        captcha = Image.open(BytesIO(captcha_content.iter_bytes().__next__()))
        return captcha

    def generate_form(self, captcha='') -> dict:
        """生成账号登录提交表单"""
        self.client.get(url=UrlConfig.home_url)
        content = self.client.get(url=UrlConfig.portal_login_url)
        form = BeautifulSoup(content.content, 'lxml').find("div", id='pwdLoginDiv')
        salt = form.find('input', id='pwdEncryptSalt').get('value')
        execution = form.find('input', id='execution').get('value')
        return {
            'username': self._account,
            'password': encrypt(self._password, salt),
            'execution': execution,
            'captcha': captcha,
            '_eventId': 'submit',
            'cllt': 'userNameLogin',
            'dllt': 'generalLogin',
            'lt': ''
        }

    def portal_user(self):
        """查询验证结果与个人信息"""
        content = self.client.get(url=UrlConfig.portal_user_url % self._current)
        return content.json()

    def login(self, captcha='') -> dict:
        """账号登录"""
        params = self.generate_form(captcha)
        self.client.post(url=UrlConfig.portal_login_url, data=params)
        self.client.get(url=UrlConfig.portal_login_service_url)
        content = self.portal_user()
        return content


class AsyncAuth(Auth):
    """南农门户异步验证类

    该类主要内容是 Auth 接口的异步实现。
    """
    def __init__(self, account, password, **kwargs):
        super(AsyncAuth, self).__init__(account, password)
        self.async_client = httpx.AsyncClient(follow_redirects=True, timeout=kwargs.get('timeout', 5))

    async def close_async_client(self):
        if not self.async_client.is_closed:
            await self.async_client.aclose()

    async def async_check_captcha(self):
        check_captcha_url = UrlConfig.portal_check_captcha_url + "?username=%s&_=%s" % (self._account, self._current)
        check_captcha_content = await self.async_client.get(check_captcha_url)
        return check_captcha_content.json()

    async def async_get_captcha(self) -> Image:
        captcha_url = UrlConfig.portal_captcha_url + "?%s" % self._current
        captcha_content = await self.async_client.get(captcha_url)
        captcha = Image.open(BytesIO(captcha_content.iter_bytes().__next__()))
        return captcha

    async def async_generate_form(self, captcha='') -> dict:
        _, content = await asyncio.gather(
            self.async_client.get(url=UrlConfig.home_url),
            self.async_client.get(url=UrlConfig.portal_login_url)
        )
        form = BeautifulSoup(content.content, 'lxml').find("div", id='pwdLoginDiv')
        salt = form.find('input', id='pwdEncryptSalt').get('value')
        execution = form.find('input', id='execution').get('value')
        return {
            'username': self._account,
            'password': encrypt(self._password, salt),
            'execution': execution,
            'captcha': captcha,
            '_eventId': 'submit',
            'cllt': 'userNameLogin',
            'dllt': 'generalLogin',
            'lt': ''
        }

    async def async_portal_user(self):
        content = await self.async_client.get(url=UrlConfig.portal_user_url % self._current)
        return content.json()

    async def async_login(self, captcha='') -> dict:
        params = await self.async_generate_form(captcha)
        await self.async_client.post(url=UrlConfig.portal_login_url, data=params),
        await self.async_client.get(url=UrlConfig.portal_login_service_url)
        content = await self.async_portal_user()
        return content
