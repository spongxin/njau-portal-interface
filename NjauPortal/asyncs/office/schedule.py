from bs4 import BeautifulSoup
from NjauPortal.config import UrlConfig
from NjauPortal.asyncs.auth import AsyncAuth
from NjauPortal.office.schedule import Schedule


class AsyncSchedule(object):
    def __init__(self, auth: AsyncAuth):
        self.auth = auth

    async def async_special_semester_schedule(self, semester, week=1) -> dict:
        await self.auth.async_client.get(url=UrlConfig.jw_xskb_url)
        content = await self.auth.async_client.post(
            url=UrlConfig.jw_course_schedule_url,
            data={'zc': week, 'sfFD': 1, 'xnxq01id': semester, 'cj0701id': ''}
        )
        soup = BeautifulSoup(content.content, 'lxml')
        return Schedule.schedule_datalist_parser(soup)

    async def async_desktop_schedule(self):
        await self.auth.async_client.get(url=UrlConfig.jw_framework_url)
        content = await self.auth.async_client.get(url=UrlConfig.jw_user_url)
        soup = BeautifulSoup(content.content, 'lxml')
        return Schedule.desktop_datalist_parser(soup)
