from bs4 import BeautifulSoup
from NjauPortal.auth import Auth
from NjauPortal.config import UrlConfig


class Schedule(object):
    """课程安排查询类

    该类主要提供学期课程与本周课程查询接口。

    """
    def __init__(self, auth: Auth):
        self.auth = auth

    def special_semester_schedule(self, semester, week=1) -> dict:
        """查询指定学期课程列表"""
        self.auth.client.get(url=UrlConfig.jw_xskb_url)
        content = self.auth.client.post(
            url=UrlConfig.jw_course_schedule_url,
            data={'zc': week, 'sfFD': 1, 'xnxq01id': semester, 'cj0701id': ''}
        )
        soup = BeautifulSoup(content.content, 'lxml')
        return self.schedule_datalist_parser(soup)

    def desktop_schedule(self):
        """查询当前周课程列表"""
        self.auth.client.get(url=UrlConfig.jw_framework_url)
        content = self.auth.client.get(url=UrlConfig.jw_user_url)
        soup = BeautifulSoup(content.content, 'lxml')
        return self.desktop_datalist_parser(soup)

    @staticmethod
    def schedule_datalist_parser(soup: BeautifulSoup, compress: bool = False) -> dict:
        table, data = soup.find("table", id="kbtable"), dict()
        if table is None:
            return data
        datalist = table.find_all("td", valign="top")
        for weekday in range(7):
            courses = list()
            for section in range(12):
                lesson = datalist[weekday + section * 7]
                if lesson.div.text == " ":
                    if not compress:
                        courses.append(dict())
                    continue
                info = list()
                title, fonts = lesson.div.text, lesson.find_all("font")
                for font in fonts[:3]:
                    info.append(font.text)
                    title = title.replace(font.text, "")
                if compress and len(courses) and courses[-1].get('title') == title:
                    courses[-1]['length'] += 1
                    continue
                courses.append({
                    "title": title,
                    "weeks": info[0],
                    "place": info[1],
                    "teacher": info[2],
                    "section": section + 1,
                    "length": 1
                })
            data[(weekday + 1)] = courses
        remark = table.find_all('tr')[-1]
        data["remark"] = remark.td.text
        return data

    @staticmethod
    def desktop_datalist_parser(soup: BeautifulSoup, compress: bool = False) -> dict:
        week, data = soup.find('div', class_='r middletopleftrqbox'), dict()
        if week is None:
            return data
        for op in ["\r", "\n", "\t", " ", "第", "周"]:
            week = week.div.text.replace(op, "")
        table = soup.find('table', class_='datalist')
        for weekday in range(1, 8):
            courses = list()
            for section in range(1, 13):
                lesson = table.find("td", id='%d_%d' % (weekday, section))
                if lesson.div.span is None:
                    if not compress:
                        courses.append(dict())
                    continue
                title = lesson.div.span.text
                course_id = lesson.div.span.get('onclick').replace("showDetails('%d_%d','" % (weekday, section), "").replace("');", "")
                if compress and len(courses) and courses[-1].get('id') == course_id:
                    courses[-1]['length'] += 1
                    continue
                courses.append({
                    "id": course_id,
                    "title": title,
                    "weekday": weekday,
                    "section": section,
                    "length": 1
                })
            data[str(weekday)] = courses
        data['week'] = week
        return data
