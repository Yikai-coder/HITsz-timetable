# coding=utf-8

import datetime
import typing

def isChinese(s) -> bool:
    if len(s) == 0:
        return False
    if u'\u4e00'<=s[0] and s[0]<=u'\u9fff':
        return True
    return False


def isTeacher(s) -> bool:
    if len(s)<2:
        return False
    return s[0]=="[" and isChinese(s[1])


def get_class_start_time(i) -> datetime.timedelta:
    td = datetime.timedelta
    if i<=2:
        if i<1:
            return td(hours=8, minutes=30)
        elif i>1:
            return td(hours=14, minutes=0)
        else:
            return td(hours=10, minutes=30)
    elif i<=5:
        if i<4:
            return td(hours=16, minutes=0)
        elif i>4:
            return td(hours=20, minutes=45)
        else:
            return td(hours=18, minutes=45)
    else:
        return td(hours=0, minutes=0)


def get_class_end_time(i) -> datetime.timedelta:
    return get_class_start_time(i) + datetime.timedelta(hours=1, minutes=45)


# returns year and semester number according to
# the date of first Monday of a semester
def semester(startDate) -> typing.Tuple[str, int]:
    year = ""
    semester = 0
    if startDate.month < 6:
        semester    = 2
        year        = str(startDate.year - 1) + '-' + str(startDate.year)
    # 增加小学期
    elif startDate.month < 8:
        semester    = 3
        year        = str(startDate.year - 1) + '-' + str(startDate.year)
    else:
        semester    = 1
        year        = str(startDate.year) + '-' + str(startDate.year + 1)
    return year, semester


def colRow2ExcelCellName(col, row) -> str:
    row_str = ""
    if row<=0:
        row_str = 'A'
    else:
        row_str = chr(ord('A') + col - 1)
    
    if col<=0:
        col = 1
    
    return row_str + str(col)



class StopLoop(RuntimeError):
    pass


class UTC(datetime.tzinfo):
    """UTC"""
    def __init__(self, offset=0):
        self._offset = offset

    def utcoffset(self, dt):
        return datetime.timedelta(hours=self._offset)

    def tzname(self, dt):
        return "UTC+%s" % self._offset

    def dst(self, dt):
        return datetime.timedelta(hours=self._offset)
