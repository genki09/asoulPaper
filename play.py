# -*- coding:utf-8 -*-

import cfg.init as gv
import requests as req
import json
import time
from bisect import bisect_left
import datetime
from datetime import timedelta


# 返回上一周开始与结束的时间戳
def lastWeekMonday():
    # 获取当前时间并重置到今天的第0秒
    now = datetime.datetime.now()
    now_str = now.strftime("%Y_%m_%d_%H_%M_%S")
    now_str_unpack = now_str.split('_')
    now_str_unpack[-3:] = ['00'] * 3
    now_str = '_'.join(now_str_unpack)
    now = datetime.datetime.strptime(now_str, "%Y_%m_%d_%H_%M_%S")

    last_week_start = now - timedelta(days=now.weekday() + 7)
    last_week_end = now - timedelta(days=now.weekday())
    last_week_start = int(time.mktime(last_week_start.timetuple())) * 1000
    last_week_end = int(time.mktime(last_week_end.timetuple())) * 1000
    return last_week_start, last_week_end


# 有序数列中寻找与目标最近的数字
def takeClosest(numlist: list, target):
    # if target > numlist[-1] or target < numlist[0]:
    #     return False
    if target < numlist[0]:
        return numlist[0]
    if target > numlist[-1]:
        return numlist[-1]

    pos = bisect_left(numlist, target)
    if pos == 0:
        return numlist[0]
    if pos == len(numlist):
        return numlist[-1]
    before = numlist[pos - 1]
    after = numlist[pos]
    if after - target < target - before:
        return after
    else:
        return before


# 13位时间戳转换函数
def timestampTrans(timestamp):
    timeArray = time.localtime(round(timestamp / 1000))
    # 这里的是文件名
    otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", timeArray)
    return otherStyleTime


# 上周内粉丝数量计算函数
def fansCal(num):
    url = 'https://api.vtbs.moe/v2/bulkActiveSome/{}'.format(gv.giveMid(num))
    r = req.get(url).text
    rt = json.loads(r)

    last_week_start, last_week_end = lastWeekMonday()

    time_list = []
    fans_list = []
    for i in rt:
        time_list.append(int(i['time']))
        fans_list.append(int(i['follower']))

    # 找到列表里离两个时间戳最近的数据记录
    time_aweek = takeClosest(time_list, last_week_start)
    fans_aweek = fans_list[time_list.index(time_aweek)]

    time_close = takeClosest(time_list, last_week_end)
    fans_close = fans_list[time_list.index(time_close)]

    print('{}：'.format(gv.giveName(num)))
    # print('{}时粉丝数为：{}'.format(timestampTrans(time_aweek), fans_aweek))
    # print('{}时粉丝数为：{}'.format(timestampTrans(time_close), fans_close))
    print('涨粉：{}'.format(fans_close - fans_aweek))


def playCal(num):
    url = 'https://api.bilibili.com/x/space/arc/search?mid={}&ps=30&tid=0&pn=1&keyword=&order=pubdate&jsonp=jsonp'
    url = url.format(gv.giveMid(num))
    r = req.get(url).text
    rt = json.loads(r)

    list_sort_by_created = []
    # 列表时间戳是从大到小排列的
    for i in rt['data']['list']['vlist']:
        list_sort_by_created.append({'play': i['play'],
                                     'title': i['title'],
                                     'time': i['created'] * 1000})

    last_week_start, last_week_end = lastWeekMonday()

    # 通过上周时间区间提取视频
    # 添加开始区间的index号实际上是要减1，具体画图理解，但是后面index[1]作为切片的第二个参数是不会读取内容的，所以此处不减1
    index_range = []
    for i in range(len(list_sort_by_created)):
        if list_sort_by_created[i]['time'] - last_week_end < 0 and not len(index_range):
            index_range.append(i)
        if list_sort_by_created[i]['time'] - last_week_start < 0 and len(index_range):
            index_range.append(i)
            break

    last_week_range = list_sort_by_created[index_range[0]:index_range[1]]
    last_week_range.sort(key=lambda info: info['play'], reverse=True)

    if len(last_week_range):
        print('本周共发布（{}）条视频，其中播放量最高为（{}）'.format(len(last_week_range), last_week_range[0]['title']))
    else:
        print('本周共发布（0）条视频')


def cardCal(num):
    url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?' \
          'visitor_uid={}&host_uid={}&offset_dynamic_id=0&need_top=1'\
          .format(712273, gv.giveMid(num))
    url = url.format(gv.giveMid(num))
    r = req.get(url).text
    rt = json.loads(r)

    cards_list = []
    dynamic_id_str = 0

    for i in rt['data']['cards']:
        tp = i['desc'].get('type')
        if tp == 4 or tp == 2:
            cards_list.append({'comment': i['desc']['comment'],
                               'card': i['card'],
                               'time': i['desc']['timestamp'] * 1000,
                               'dynamic_id_str': i['desc']['dynamic_id_str']})
            dynamic_id_str = i['desc']['dynamic_id_str']

    url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?' \
          'visitor_uid={}&host_uid={}&offset_dynamic_id={}&need_top=1'\
          .format(712273, gv.giveMid(num), dynamic_id_str)
    url = url.format(gv.giveMid(num))
    r = req.get(url).text
    rt = json.loads(r)

    for i in rt['data']['cards']:
        tp = i['desc'].get('type')
        if tp == 4 or tp == 2:
            cards_list.append({'comment': i['desc']['comment'],
                               'card': i['card'],
                               'time': i['desc']['timestamp'] * 1000,
                               'dynamic_id_str': i['desc']['dynamic_id_str']})

    last_week_start, last_week_end = lastWeekMonday()

    cards_list.sort(key=lambda info: info['time'], reverse=True)

    index_range = []
    for i in range(len(cards_list)):
        if cards_list[i]['time'] - last_week_end < 0 and not len(index_range):
            index_range.append(i)
        if cards_list[i]['time'] - last_week_start < 0 and len(index_range):
            index_range.append(i)
            break

    last_week_range = cards_list[index_range[0]:index_range[1]]
    last_week_range.sort(key=lambda info: info['comment'], reverse=True)

    # 按照评论数量逆序排序完成，last_week_range[0]即为评论最高信息
    print('本周共发布（{}）条动态，其中评论最高为:'.format(len(last_week_range)))
    print('----------------------------------')
    if len(last_week_range):
        card_content = json.loads(last_week_range[0]['card'])['item']
        if card_content.get('content'):
            print(card_content['content'] + '\n')
        elif card_content.get('description'):
            print(card_content['description'] + '\n')

        print('https://t.bilibili.com/{}?tab=2'.format(last_week_range[0]['dynamic_id_str']))
    print('----------------------------------')


def accFansTime(fans_num, mem_id):
    url = 'https://api.vtbs.moe/v2/bulkActiveSome/{}'.format(gv.giveMid(mem_id))
    r = req.get(url).text
    rt = json.loads(r)

    time_list = []
    fans_list = []
    for i in rt:
        time_list.append(int(i['time']))
        fans_list.append(int(i['follower']))

    fans_close = takeClosest(fans_list, fans_num)
    time_close = time_list[fans_list.index(fans_close)]

    print(timestampTrans(time_close))


if __name__ == '__main__':
    accFansTime(200000, 1)
