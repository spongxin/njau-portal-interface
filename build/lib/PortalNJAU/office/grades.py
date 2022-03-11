from ..config import UrlConfig
from ..auth import Auth, AsyncAuth
from bs4 import BeautifulSoup


class Grade(object):
    """课程成绩查询类

    该类主要提供成绩查询接口。

    """
    def __init__(self, auth: Auth):
        self.auth = auth

    def total_semester_grade(self) -> list:
        """在校成绩列表"""
        self.auth.client.get(url=UrlConfig.jw_grade_kscj_url)
        content = self.auth.client.get(url=UrlConfig.jw_grade_total_url)
        soup = BeautifulSoup(content.content, "lxml")
        datalist = self.grades_datalist_parser(soup)
        return datalist

    def current_semester_grade(self) -> list:
        """当学期成绩列表"""
        self.auth.client.get(url=UrlConfig.jw_grade_kscj_url)
        content = self.auth.client.get(url=UrlConfig.jw_grade_current_url)
        soup = BeautifulSoup(content.content, "lxml")
        datalist = self.grades_datalist_parser(soup)
        return datalist

    def total_archive_grade(self) -> list:
        """归档成绩列表"""
        self.auth.client.get(url=UrlConfig.jw_grade_kscj_url)
        content = self.auth.client.get(url=UrlConfig.jw_grade_archive_url)
        soup = BeautifulSoup(content.content, "lxml")
        datalist = self.grades_datalist_parser(soup, 1)
        return datalist

    @staticmethod
    def grades_datalist_parser(soup: BeautifulSoup, index=0) -> list:
        table, datalist = soup.find("table", id="dataList"), list()
        if table is None or "未查询到数据" in table.text:
            return datalist
        trs = table.find_all("tr")
        keys = [th.text for th in trs.__getitem__(index).find_all("th")]
        for tr in trs[index + 1:]:
            tds, info = tr.find_all("td"), dict()
            for i in range(len(keys)):
                info[keys[i]] = tds[i].text
            datalist.append(info)
        return datalist


class AsyncGrade(object):
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
