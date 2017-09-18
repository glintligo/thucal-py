#! usr/bin/python
#coding=utf-8
import xlrd
import re
import datetime
import codecs
from ics import Calendar, Event

class Course:
    s = ""
    name = ""
    teacher = ""
    time = ""
    type = ""
    weeks = ""
    weekday = 0
    site = ""
    date = ""

    def resolve(self):
        s_split = self.s.split('；')
        s_t = s_split[0].split('(')
        self.name = s_t[0]
        self.teacher = s_t[1]
        self.type = s_split[1]
        self.site = s_split[3][0:len(self.site)-1]
        if( s_split[2] == "全周"):
            self.weeks = range(1, 16)
        if (s_split[2] == "前八周"):
            self.weeks = range(1, 8)
        if (s_split[2] == "后八周"):
            self.weeks = range(9, 16)
        if (s_split[2] == "单周"):
            self.weeks = range(1, 16, 2)
        if (s_split[2] == "双周"):
            self.weeks = range(2, 16, 2)
        s1=re.findall("\\d.*?-",s_split[2])
        s2=re.findall("-.*?周",s_split[2])
        if(len(s1) != 0):
            self.weeks = range(int(s1[0][0:len(s1[0])-1]), int(s2[0][1:len(s2[0])-1]))


def generate_date(course_tmp):
    begin_day = datetime.datetime(2017,9,18)
    date_list = []
    for d in course_tmp.weeks:
        date_list.append(begin_day+datetime.timedelta(days=(d-1)*7+course_tmp.weekday-1))
    course_tmp.weeks = date_list


if __name__ == "__main__":
    cal = Calendar()
    filename = "cal.xls"
    sheet_name = "report"
    time = [8, 9+5/6, 13.5, 15+1/3, 17+1/12, 19+1/3]
    book = xlrd.open_workbook(filename)
    sheet = book.sheet_by_name(sheet_name)
    li = []
    event = Event()
    for i in range(1, sheet.ncols):
        for j in range(2, sheet.nrows):
            if sheet.cell(j, i).value != '':
                course = Course()
                course.s = sheet.cell(j, i).value
                course.time = time[j-2]
                course.weekday = i
                course.resolve()
                li.append(course)
    for course in li:
        generate_date(course)
        event.name = course.name
        event.description = course.teacher + " " + course.type
        event.location = course.site
        for date in course.weeks:
            event.begin = date+datetime.timedelta(hours=course.time-8)
            event.duration = datetime.timedelta(hours=1.5+1/12)
            print(event)
            cal.events.append(event)
            event = event.clone()
    print(cal)
    with codecs.open("cal.ics", "w", encoding="utf8") as f:
        f.writelines(cal)


