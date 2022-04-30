from bs4 import BeautifulSoup
from NjauPortal.config import UrlConfig
from NjauPortal.office.grades import Grade
from NjauPortal.asyncs.auth import AsyncAuth


class AsyncGrade:
    """课程成绩异步查询类

    该类主要提供成绩异步查询接口。

    """
    def __init__(self, auth: AsyncAuth):
        self.auth = auth

    async def async_total_semester_grade(self) -> list:
        """在校成绩列表"""
        await self.auth.async_client.get(url=UrlConfig.jw_grade_kscj_url)
        content = await self.auth.async_client.get(url=UrlConfig.jw_grade_total_url)
        soup = BeautifulSoup(content.content, "lxml")
        datalist = Grade.grades_datalist_parser(soup)
        return datalist

    async def async_current_semester_grade(self) -> list:
        """当学期成绩列表"""
        await self.auth.async_client.get(url=UrlConfig.jw_grade_kscj_url)
        content = await self.auth.async_client.get(url=UrlConfig.jw_grade_current_url)
        soup = BeautifulSoup(content.content, "lxml")
        datalist = Grade.grades_datalist_parser(soup)
        return datalist

    async def async_total_archive_grade(self) -> list:
        """归档成绩列表"""
        await self.auth.async_client.get(url=UrlConfig.jw_grade_kscj_url)
        content = await self.auth.async_client.get(url=UrlConfig.jw_grade_archive_url)
        soup = BeautifulSoup(content.content, "lxml")
        datalist = Grade.grades_datalist_parser(soup, 1)
        return datalist
