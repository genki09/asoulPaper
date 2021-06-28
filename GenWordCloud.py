# -*- coding: utf-8 -*-

import re
import json
import jieba
import numpy as np
from PIL import Image
from cfg.init import Global
from wordcloud import WordCloud, ImageColorGenerator

GValue = Global(0, False)


def isNumLeters(s):
    if not s:
        return False
    else:
        return True if re.match(r'^[0-9a-zA-Z]+$', s) else False


# 寻找数字、字母的最长字串，并合并，以及添加词频频率
def keySet(frequent: dict):
    fre2 = {}
    pop_list = []
    for key in frequent:
        # 判断是否为全部数字字母组成
        if isNumLeters(key):
            # 保存原键值，if语段中使用的key变量都是小写版本
            keyOri = key
            key = key.lower()
            # 判断是否为由多个重复子串组成
            if key in (key + key)[1:-1]:
                # 先去重变成列表
                lst = list(set(key))
                # 对列表进行排序再组回字符串
                lst.sort(key=key.index)
                keyset = ''.join(lst)
                # 去重后的字符串的二倍不能小于等于原字符串
                if len(keyset) * 2 < len(key):
                    fre2.setdefault(keyset, 0)
                    fre2[keyset] += frequent[keyOri]
                    pop_list.append(keyOri)
    # 按照合并的词频从高到低打印
    print(sorted(fre2.items(), key=lambda x: x[1], reverse=True))
    print(pop_list)
    frequent.update(fre2)
    for item in pop_list:
        frequent.pop(item)
    return frequent


def sendGlobal(value: Global):
    global GValue
    GValue = value


def danmakuFactory(danmaku_name: str):

    jieba.load_userdict("./cfg/ASdict.txt")

    # 读取从matsuri.icu下载的弹幕json
    with open("./json/{}/{}.json".format(GValue.FLODERNAME, danmaku_name)) as danmaku:
        data = json.load(danmaku)
        comment_list = data["data"]

        comments_str = ""
        # 把所有弹幕存进字符串
        for text in comment_list:
            if 'text' in text:
                comments_str = comments_str + ' ' + text["text"]

    # 分词
    dic = {}
    resource = jieba.lcut(comments_str)

    # 载入stopwords(被除外的词)
    exclude = set()
    content = [line.strip() for line in open('./cfg/exclude.txt', 'r', encoding='UTF-8').readlines()]
    exclude.update(content)

    # 计算频率，单字不计入 stopwords不计入
    for word in resource:
        if word in exclude:
            continue
        else:
            # 把下面两行注释了就计入单字
            if len(word) == 1:
                continue
            if word in dic:
                dic[word] += 1
            else:
                dic[word] = 1
    dic = list(dic.items())

    frequent = {}
    for i in range(len(dic)):
        frequent[dic[i][0]] = dic[i][1]
    # with open('./cfg/frequent.txt', 'w+', encoding='UTF-8') as f:
    #     print(frequent, file=f)

    # 读取同义词字典
    combine_dict = {}
    with open('./cfg/combine.txt', 'r', encoding='UTF-8') as f_combine:
        for line in f_combine:
            s_key = line.strip().split("-")[0]
            s_value = line.strip().split("-")[1]
            if s_value != "":
                if s_key in combine_dict:
                    combine_dict.get(s_key).append(s_value)
                else:
                    combine_dict.setdefault(s_key, []).append(s_value)

    """到此处计算、分词已经全部处理完毕，出于美观与成品质量，下面开始对得到的频率数据进行二次处理"""

    # 合并同义词
    for key in combine_dict.keys():
        if key not in frequent:
            frequent.setdefault(key, 0)
        for same in combine_dict[key]:
            if same in frequent:
                frequent[key] += frequent[same]
                frequent.pop(same)

    # 寻找由数字字母组成的关键词的最长重复子串，并合并词频频率
    frequent = keySet(frequent)

    # 将只有大小不同的键全部合并为小写
    repeat = []
    for key in frequent:
        key_low = key.lower()
        if key_low != key and frequent.get(key_low):
            frequent[key_low] += frequent[key]
            repeat.append(key)
    for i in repeat:
        frequent.pop(i)

    # 重设部分词频频率
    for key in GValue.FREQUENT:
        frequent[key] *= GValue.FREQUENT[key]

    # 更改键名，实质上是在对前面工作处理完之后出现语义遗失的补救工作
    # frequent['000000000'] = frequent.pop('0')
    frequent['收到收到收到'] = frequent.pop('收到')
    frequent['hhhh'] = frequent.pop('h')
    frequent['66666'] = frequent.pop('6')
    frequent['777777'] = frequent.pop('7')
    frequent['8888888'] = frequent.pop('8')

    # 打印频率结果文件并返回频率词典
    with open('./cfg/frequent_combined.txt', 'w+', encoding='UTF-8') as f:
        print(frequent, file=f)
    return frequent


def cloudMaker(frequent: dict):
    mask = np.array(Image.open("./pic/{}/{}".format(GValue.FLODERNAME, GValue.MASKPATH)))

    # 生成词云图
    image_colors = ImageColorGenerator(mask)
    if GValue.groupflag:
        max_words = 750
    else:
        max_words = 500
    wordcloud = WordCloud(width=1080, height=1920,
                          font_path="/Users/apple/Downloads/晴圆.ttc", background_color="white",
                          # max_font_size=12,
                          # min_font_size=2,
                          max_words=max_words, mask=mask,
                          relative_scaling=0.4,
                          color_func=image_colors).generate_from_frequencies(frequent)
    wordcloud.to_file("./out/{}/{}.png".format(GValue.FLODERNAME, GValue.FILENAME))
    print('Done!')
