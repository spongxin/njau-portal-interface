# -*- coding: utf-8 -*-
import time
import httpx
from io import BytesIO
from bs4 import BeautifulSoup
from NjauPortal.encrypt import encrypt
from NjauPortal.config import UrlConfig


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

    def _generate_form(self, captcha='') -> dict:
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

    def _portal_user(self):
        """查询验证结果与个人信息"""
        content = self.client.get(url=UrlConfig.portal_user_url % self._current)
        return content.json()
    
    def _check_captcha(self) -> dict:
        """检查账号登录是否需要验证（isNeed）"""
        check_captcha_url = UrlConfig.portal_check_captcha_url + "?username=%s&_=%s" % (self._account, self._current)
        check_captcha_content = self.client.get(check_captcha_url)
        return check_captcha_content.json()

    def get_captcha(self) -> BytesIO:
        """获取登录验证码（BytesIO）"""
        if not self._check_captcha().get('isNeed', False):
            return None
        captcha_url = UrlConfig.portal_captcha_url + "?%s" % self._current
        captcha_content = self.client.get(captcha_url)
        captcha = BytesIO(captcha_content.iter_bytes().__next__())
        return captcha

    def login(self, captcha='') -> dict:
        """账号登录"""
        params = self._generate_form(captcha)
        self.client.post(url=UrlConfig.portal_login_url, data=params)
        self.client.get(url=UrlConfig.portal_login_service_url)
        content = self._portal_user()
        return content

