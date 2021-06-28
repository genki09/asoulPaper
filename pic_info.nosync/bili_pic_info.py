# -*- coding: utf-8 -*-

import json
import os
import sys
from contextlib import closing

import requests

info_url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id={}'


def download_file(file_name, file_type, file_url, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    file_path = os.path.join(save_dir, file_name) + '.' + file_type
    if os.path.isfile(file_path):
        print('---{}文件已存在...\r'.format(file_path))
    else:
        print('---{}开始下载...\r'.format(file_path).encode('utf-8'))
        size = 0
        with closing(requests.get(file_url, stream=True)) as response:
            chunk_size = 1024
            content_size = int(response.headers['content-length'])
            if response.status_code == 200:
                sys.stdout.write('----[文件大小]:%0.2f MB\n' % (content_size / chunk_size / 1024))

                with open(file_path, 'wb') as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        size += len(data)
                        file.flush()
                        sys.stdout.write('----[下载进度]:%.2f%%' % float(size / content_size * 100) + '\r')
                        sys.stdout.flush()


def get_info(bv_id):
    response = requests.get(info_url.format(bv_id))
    result = response.json()
    if result.get('code') == 0:
        data = result['data']
        if data.get('card'):
            card_str = data['card']['card']
            card = json.loads(card_str)
            user_name = card['user']['name']
            pictures_list = card['item']['pictures']
            pic_url_list = []
            for picture in pictures_list:
                pic_url_list.append(picture['img_src'])
            return user_name, pic_url_list
        else:
            return False, False


def run(pic_url, save_dir):
    user_name, pic_url_list = get_info(pic_url)
    if user_name and pic_url_list:
        save_dir = os.path.join(save_dir, user_name)
        i = 1
        for down_url in pic_url_list:
            # 之前的命名方式
            # download_file(down_url.split('/').pop().split('.')[0], 'jpg', down_url, save_dir)

            # 使用链接命名
            download_file(pic_url.split('?')[0] + '%3Ftab=' + str(i), 'jpg', down_url, save_dir)
            i += 1


if __name__ == "__main__":
    txt_path = './pic_list.txt'

    if not os.path.isfile(txt_path):
        print('缺少txt文件')
    else:
        dir_input = input('输入下载文件夹名称 (默认为"Download"):')
        dir_input = './{}/'.format(dir_input) if dir_input else "./Download/"
        with open(txt_path, 'r') as f:
            dynamic_url_list = f.readlines()
            for dynamic_url in dynamic_url_list:
                dynamic_url = dynamic_url.replace('\n', '')
                if 'https://t.bilibili.com/' in dynamic_url:
                    run(dynamic_url.split('/').pop(), dir_input)
