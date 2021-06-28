# -*- coding:utf-8 -*-

class Global:
    def __init__(self, ini: int, group: bool):
        self.ini = ini
        if group:
            self.groupflag = True
        else:
            self.groupflag = False
        self.FLODERNAME = ''
        self.FILENAME = ''
        self.MASKPATH = ''
        self.LIVEID = ''
        self.FREQUENT = {}

    def set_flodername(self):
        if not self.groupflag:
            if self.ini == 1:
                self.FLODERNAME = 'ava'
            elif self.ini == 2:
                self.FLODERNAME = 'bella'
            elif self.ini == 3:
                self.FLODERNAME = 'carol'
            elif self.ini == 4:
                self.FLODERNAME = 'diana'
            elif self.ini == 5:
                self.FLODERNAME = 'eileen'
        else:
            self.FLODERNAME = 'group'

    def set_filename(self, name: str):
        self.FILENAME = name

    def set_maskpath(self, name: str):
        self.MASKPATH = name

    def set_liveid(self):
        if self.ini == 1:
            self.LIVEID = '672346917'
        elif self.ini == 2:
            self.LIVEID = '672353429'
        elif self.ini == 3:
            self.LIVEID = '351609538'
        elif self.ini == 4:
            self.LIVEID = '672328094'
        elif self.ini == 5:
            self.LIVEID = '672342685'

    def set_frequent(self, setting: dict):
        self.FREQUENT = setting


def giveName(ini):
    if ini == 1:
        return '向晚'
    elif ini == 2:
        return '贝拉'
    elif ini == 3:
        return '珈乐'
    elif ini == 4:
        return '嘉然'
    elif ini == 5:
        return '乃琳'
    elif ini == 6:
        return '官方'


def giveMid(ini):
    if ini == 1:
        return '672346917'
    elif ini == 2:
        return '672353429'
    elif ini == 3:
        return '351609538'
    elif ini == 4:
        return '672328094'
    elif ini == 5:
        return '672342685'
    elif ini == 6:
        return '703007996'


def giveRoom(ini):
    if ini == 1:
        return '22625025'
    elif ini == 2:
        return '22632424'
    elif ini == 3:
        return '351609538'
    elif ini == 4:
        return '672328094'
    elif ini == 5:
        return '672342685'
