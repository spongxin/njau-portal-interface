from ..config import UrlConfig
from ..auth import Auth, AsyncAuth
from bs4 import BeautifulSoup


class Exam(object):
    """考试安排查询类

    该类主要提供学期考试安排接口。

    """
    def __init__(self, auth: Auth):
        self.auth = auth

    def special_semester_exam(self, semester) -> list:
        """查询指定学期考试安排"""
        self.auth.client.get(url=UrlConfig.jw_xsks_url)
        content = self.auth.client.post(
            url=UrlConfig.jw_exam_detail_url,
            data={'xqlbmc': '', 'xnxqid': semester}
        )
        soup = BeautifulSoup(content.content, 'lxml')
        return self.exams_datalist_parser(soup)

    @staticmethod
    def exams_datalist_parser(soup: BeautifulSoup) -> list:
        table, datalist = soup.find('table', id="dataList"), list()
        if table is None or '未查询到数据' in table.text:
            return datalist
        keys = [th.text for th in table.tr.find_all('th')]
        for tr in table.find_all('tr')[1:]:
            tds, info = tr.find_all('td'), dict()
            for i in range(len(keys)):
                info[keys[i]] = tds[i].text
            datalist.append(info)
        return datalist


class AsyncExam(object):
    def __init__(self, auth: AsyncAuth):
        self.auth = auth

    async def async_semester_exam(self, semester) -> list:
        """查询指定学期考试安排"""
        await self.auth.async_client.get(url=UrlConfig.jw_xsks_url)
        content = await self.auth.async_client.post(
            url=UrlConfig.jw_exam_detail_url,
            data={'xqlbmc': '', 'xnxqid': semester}
        )
        soup = BeautifulSoup(content.content, 'lxml')
        return Exam.exams_datalist_parser(soup)
