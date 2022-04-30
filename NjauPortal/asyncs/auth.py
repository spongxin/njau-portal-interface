# -*- coding: utf-8 -*-
import time
import httpx
import asyncio
from io import BytesIO
from bs4 import BeautifulSoup
from NjauPortal.encrypt import encrypt
from NjauPortal.config import UrlConfig



class AsyncAuth:
    """南农门户异步验证类

    该类主要内容是 Auth 接口的异步实现。
    """
    def __init__(self, account, password, **kwargs):
        self._account = account
        self._password = password
        self._current = int(time.time() * 1000)
        self.async_client = httpx.AsyncClient(follow_redirects=True, timeout=kwargs.get('timeout', 5))

    async def close_async_client(self):
        if not self.async_client.is_closed:
            await self.async_client.aclose()

    async def _async_check_captcha(self):
        check_captcha_url = UrlConfig.portal_check_captcha_url + "?username=%s&_=%s" % (self._account, self._current)
        check_captcha_content = await self.async_client.get(check_captcha_url)
        return check_captcha_content.json()

    async def async_get_captcha(self) -> BytesIO:
        if not await self._async_check_captcha().get('isNeed', False):
            return None
        captcha_url = UrlConfig.portal_captcha_url + "?%s" % self._current
        captcha_content = await self.async_client.get(captcha_url)
        captcha = BytesIO(captcha_content.iter_bytes().__next__())
        return captcha

    async def _async_generate_form(self, captcha='') -> dict:
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

    async def _async_portal_user(self):
        content = await self.async_client.get(url=UrlConfig.portal_user_url % self._current)
        return content.json()

    async def async_login(self, captcha='') -> dict:
        params = await self._async_generate_form(captcha)
        await self.async_client.post(url=UrlConfig.portal_login_url, data=params),
        await self.async_client.get(url=UrlConfig.portal_login_service_url)
        content = await self._async_portal_user()
        return content

