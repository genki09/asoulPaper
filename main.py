# -*- coding:utf-8 -*-

import os
import sys
import time
import play
import json
import xmltodict
import requests as req
import GenWordCloud as wc
from cfg.init import Global

# 1：向晚
# 2：贝拉
# 3：珈乐
# 4：嘉然
# 5：乃琳
# 团播需要设置group属性
GValue = Global(4, group=True)
# 要加文件后缀，上面设置的人/组对应文件夹里一定要有这张图片
GValue.set_maskpath('5人深色.jpg')
GValue.set_flodername()
GValue.set_liveid()
GValue.set_frequent({'好': 0.75,
                     '快快': 0.70,
                     '老公': 1.05,
                     })


# json保存函数
def saveJson(save_path, data):
    assert save_path.split('.')[-1] == 'json'
    with open(save_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)


# 使用matsuri.icu请求参数中对应人员的直播参数
def danmakuIdRequest():
    url = "https://api.matsuri.icu/channel/{}/clips".format(GValue.LIVEID)
    r = req.get(url).text
    rt = json.loads(r)
    if rt['status'] == 0:
        return rt
    else:
        return


# 获取近三次直播信息
def getNear3(rt):
    for n in range(3):
        time_start = " 开始时间：" + play.timestampTrans(rt['data'][n]['start_time'])
        time_stop = " 结束时间：" + play.timestampTrans(rt['data'][n]['end_time'])
        danmaku_num = " 弹幕数：" + str(rt['data'][n]['total_danmu'])
        view_num = " 观看数：" + str(rt['data'][n]['views'])
        print(str(n) + " 直播标题：" + rt['data'][n]['title'] + time_start + time_stop + danmaku_num + view_num)
    number = int(input("请输入要获取弹幕直播编号："))
    filen = play.timestampTrans(rt['data'][number]['start_time'])
    # 在这里设置的文件名
    GValue.set_filename(filen)
    return rt['data'][number]['id']


# 弹幕下载函数
def downloadDanmakuJson(liveid):
    url = "https://api.matsuri.icu/clip/{}/comments".format(liveid)
    r = req.get(url).text
    rt = json.loads(r)
    saveJson("./json/{}/{}.json".format(GValue.FLODERNAME, GValue.FILENAME), rt)


# 定义xml转json的函数
def xml_to_json(xml_str):
    # parse是的xml解析器
    xml_parse = xmltodict.parse(xml_str)
    # json库dumps()是将dict转化成json格式,loads()是将json转化成dict格式。
    # dumps()方法的ident=1,格式化json
    json_str = json.dumps(xml_parse, indent=1)
    return json_str


# 综合数据统计函数
def dataWeekCal():
    last_week_start, last_week_end = play.lastWeekMonday()
    last_week_start = play.timestampTrans(last_week_start)
    last_week_end = play.timestampTrans(last_week_end)

    origin = sys.stdout
    f = open('./recordHistory/{}.txt'.format(last_week_start), 'w+')
    sys.stdout = f
    print("数据统计时间段：{} -> {}\n".format(last_week_start, last_week_end))
    for num in range(1, 7):
        play.fansCal(num)
        play.playCal(num)
        play.cardCal(num)
    sys.stdout = origin
    f.close()


if __name__ == '__main__':
    # """下载弹幕"""
    # live_id = getNear3(danmakuIdRequest())
    # if not os.path.exists("./json/{}/{}.json".format(GValue.FLODERNAME, GValue.FILENAME)):
    #     downloadDanmakuJson(live_id)
    #     for i in [0, 1, 2, 3] * 3:
    #         print("\r正在下载弹幕" + '.' * i, end='', flush=True)
    #         time.sleep(0.25)
    #     print("\n{}下载完成，开始制作词云".format(GValue.FILENAME))
    # else:
    #     print("{}已存在，开始制作词云".format(GValue.FILENAME))
    #
    # """制作词云"""
    # # 如果要手动设置json文件的话在这里输入文件名，不用加后缀名
    # # GValue.FILENAME = 'b'
    #
    # # 这里把设置的全局变量传到GenWordCloud里
    # wc.sendGlobal(GValue)
    # wc.cloudMaker(wc.danmakuFactory(GValue.FILENAME))

    """数据提取"""
    dataWeekCal()
