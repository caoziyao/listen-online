# from replay import *

from bs4 import BeautifulSoup
from flask import url_for
from flask import Flask


import requests
import json
import os
import time
import base64
import hashlib
import os.path
import pyaes
import binascii
import logging
import os.path
import sys
import urllib
import gzip
import io
try:
    from StringIO import StringIO as stringIOModule
except ImportError:
    from io import StringIO as stringIOModule


# 导入:
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table,Column,Integer,String,MetaData,ForeignKey  
# 创建对象的基类:
Base = declarative_base()


# 初始化数据库连接:
engine=create_engine('sqlite:///play.sqlite',echo=True) 


from models.play import Album
from models.play import Playlist
 

'''
网易云音乐 Api
'''
# 歌曲榜单地址
top_list_all = {
    0: ['云音乐新歌榜', '/discover/toplist?id=3779629'],
    1: ['云音乐热歌榜', '/discover/toplist?id=3778678'],
    2: ['网易原创歌曲榜', '/discover/toplist?id=2884035'],
    3: ['云音乐飙升榜', '/discover/toplist?id=19723756'],
    4: ['云音乐电音榜', '/discover/toplist?id=10520166'],
    5: ['UK排行榜周榜', '/discover/toplist?id=180106'],
    6: ['美国Billboard周榜', '/discover/toplist?id=60198'],
    7: ['KTV嗨榜', '/discover/toplist?id=21845217'],
    8: ['iTunes榜', '/discover/toplist?id=11641012'],
    9: ['Hit FM Top榜', '/discover/toplist?id=120001'],
    10: ['日本Oricon周榜', '/discover/toplist?id=60131'],
    11: ['韩国Melon排行榜周榜', '/discover/toplist?id=3733003'],
    12: ['韩国Mnet排行榜周榜', '/discover/toplist?id=60255'],
    13: ['韩国Melon原声周榜', '/discover/toplist?id=46772709'],
    14: ['中国TOP排行榜(港台榜)', '/discover/toplist?id=112504'],
    15: ['中国TOP排行榜(内地榜)', '/discover/toplist?id=64016'],
    16: ['香港电台中文歌曲龙虎榜', '/discover/toplist?id=10169002'],
    17: ['华语金曲榜', '/discover/toplist?id=4395559'],
    18: ['中国嘻哈榜', '/discover/toplist?id=1899724'],
    19: ['法国 NRJ EuroHot 30周榜', '/discover/toplist?id=27135204'],
    20: ['台湾Hito排行榜', '/discover/toplist?id=112463'],
    21: ['Beatport全球电子舞曲榜', '/discover/toplist?id=3812895']
}

default_timeout = 10

# 获取高音质mp3 url
def geturl(song):
    pass

header = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'text/html;charset=utf8',
        'Host': 'music.163.com',
        'Referer': 'https://www.google.co.jp/',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
        #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    }

# 歌曲加密算法, 基于https://github.com/yanunon/NeteaseCloudMusic脚本实现
def _encrypted_id(id):
    magic = bytearray('3go8&$8*3*3h0k(2)2')
    song_id = bytearray(id)
    magic_len = len(magic)
    for i in range(len(song_id)):
        song_id[i] = song_id[i] ^ magic[i % magic_len]
    m = hashlib.md5(song_id)
    result = m.digest().encode('base64')[:-1]
    result = result.replace('/', '_')
    result = result.replace('+', '-')
    return result

modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b72' + \
          '5152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbd' + \
          'a92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe48' + \
          '75d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
nonce = '0CoJUm6Qyw8W8jud'
pubKey = '010001'

def _create_secret_key_old(size):
    randlist = map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))
    return (''.join(randlist))[0:16]

def _create_secret_key(size):
    randlist = map(lambda xx: (hex(ord(chr(xx)))[2:]), os.urandom(size))
    return (''.join(randlist))[0:16]

# python 2
# aes = pyaes.AESModeOfOperationCBC(sec_key, iv='0102030405060708')
# ciphertext = b''
# return ciphertext
def _aes_encrypt(text, sec_key):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    aes = pyaes.AESModeOfOperationCBC(sec_key.encode("utf-8"), iv='0102030405060708')
    ciphertext = b''
    while text != '':
        ciphertext += aes.encrypt(text[:16])
        text = text[16:]
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext.decode('utf-8')

# The hex codec has been chucked in 3.x. Use binascii instead:
# python 2
# rs = int(text.encode('hex'), 16) ** int(pubKey, 16) % int(modulus, 16)
def _rsa_encrypt(text, pub_key, modulus):
    text = text[::-1]
    rs = int(binascii.hexlify(text.encode('utf-8')), 16) ** int(pubKey, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)

def _encrypted_request(text):
    text = json.dumps(text)
    sec_key = _create_secret_key(16)
    enc_text = _aes_encrypt(_aes_encrypt(text, nonce), sec_key)
    enc_sec_key = _rsa_encrypt(sec_key, pubKey, modulus)
    data = {
        'params': enc_text,
        'encSecKey': enc_sec_key
    }
    return data

########################################
# network
########################################
def chunk_report(bytes_so_far, chunk_size, total_size):
    percent = float(bytes_so_far) / total_size
    percent = round(percent * 100, 2)
    sys.stdout.write(
        "Downloaded %d of %d bytes (%0.2f%%)\r" %
        (bytes_so_far, total_size, percent))

    if bytes_so_far >= total_size:
        sys.stdout.write('\n')

def chunk_read(response, chunk_size=8192, report_hook=None):
    total_size = response.info().getheader('Content-Length').strip()
    total_size = int(total_size)
    bytes_so_far = 0

    total = ''
    while 1:
        chunk = response.read(chunk_size)
        bytes_so_far += len(chunk)

        if not chunk:
            break
        total += chunk
        if report_hook:
            report_hook(bytes_so_far, chunk_size, total_size)
    return total

"""
python 3.x中urllib库和urilib2库合并成了urllib库。。
其中urllib2.urlopen()变成了urllib.request.urlopen()
       urllib2.Request()变成了urllib.request.Request()
"""
# python2
# data = urllib.urlencode(v) if v else None
# data = urllib.parse.urlencode(v) if v else None
# buf = StringIO.StringIO(result)
logger = logging.getLogger('listenone.' + __name__)
def h(
        url, v=None, progress=False, extra_headers={},
        post_handler=None, return_post=False):
    '''
    base http request
    progress: show progress information
    need_auth: need douban account login
    '''
    logger.debug('fetching url:' + url)
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) ' + \
                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86' + \
                 ' Safari/537.36'
    headers = {'User-Agent': user_agent}
    headers.update(extra_headers)

    data = urllib.parse.urlencode(v).encode("utf-8") if v else None
    req = urllib.request.Request(url, data, headers)
    # POST data should be bytes or an iterable of bytes. It cannot be of type str
    # req = req.encode('utf-8')
    response = urllib.request.urlopen(req)
    if progress:
        result = chunk_read(response, report_hook=chunk_report)
    else:
        result = response.read()
    # python 3
    # The content is compressed with gzip. You need to decompress it:
    result = gzip.decompress(result).decode('utf-8')
    # print(result)
    # if response.info().get('Content-Encoding') == 'gzip':
    #     # note
    #     buf = io.StringIO(result)
    #     f = gzip.GzipFile(fileobj=buf)
    #     result = f.read()
    # if post_handler:
    #     post_result = post_handler(response, result)
    #     if return_post:
    #         return post_result
    return result


def _ne_h(url, v=None):
    # http request
    extra_headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'music.163.com',
        'Referer': 'http://music.163.com/search/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2)' +
        ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome' +
        '/33.0.1750.152 Safari/537.36'
    }
    return h(url, v=v, extra_headers=extra_headers)


# 歌单（网友精选碟） hot||new http://music.163.com/#/discover/playlist/
def top_playlist(category='华语', order='hot', offset=0, limit=50):
    """
    返回 标题、封面图片、url
    """
    action = 'http://music.163.com/discover/playlist/?cat=' + category
    # try:
    data = requests.get(action)
    soup = BeautifulSoup(data.text, 'lxml')

    host = 'http://music.163.com/#'
    divs = soup.select('div.u-cover')
    album = []
    for div in divs:
        img_url = div.find('img', attrs={"class": "j-flag"})['src']
        title = div.find('a', attrs={'class': 'msk'})['title']
        url = host + div.find('a', attrs={'class': 'msk'})['href']
        album_id = div.find('a', attrs={'class': 'icon-play'})['data-res-id']
        album_id = int(album_id)
        # print(album_id)
        # print(title, img_url, url)
        album.append({'title': title, 'cover_img_url': img_url, 'url': url, 'album_id': album_id})

    # d = dict(playlist=[], album=album)

    for al in album:
        a = Album(al)
        a.nusicfm_id = 2    # 2 代表 doubanFM
        a.save()

    return album

def song_img(song_id):
    action = 'http://music.163.com/m/song/{}?autoplay=true'.format(song_id)
    header = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36'
    }
    data = requests.get(action, headers=header)
    soup = BeautifulSoup(data.text, 'lxml')
    # print(soup)
    # url = soup.find('img', attrs={"class": "j-img"})['src']
    url = soup.select('div.img img')[0]['src']
    # print(url)
    time.sleep(1)
    return url


# 每首歌详情
def song_url(song_id):
    """
    返回 歌播放地址
    """
    action = 'http://music.163.com/weapi/song/enhance/player/url'
    # song_id = 81807
    csrf = ''
    d = {
        "ids": [song_id],
        "br": 12800,
        "csrf_token": csrf
    }
    # url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
    request = _encrypted_request(d)
    response = json.loads(_ne_h(action, request))
    # print('respones', response)
    url = response.get('data')[0].get('url')
    # print(url)
    time.sleep(1)
    return url


# 歌单详情
def playlist_detail(album):
    """
    返回 歌单列表
    """
    # action = 'http://music.163.com/m/playlist?id=496240695'
    header = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36'
    }
    # action = 'http://music.163.com/#/playlist?id=496240695'
    # 变成 action = 'http://music.163.com/m/playlist?id=496240695'
    action = album.get('url').replace('#', 'm')
    print('geting from', action)
    # time.sleep(2)
    data = requests.get(action, headers=header)
    soup = BeautifulSoup(data.text, 'lxml')
    lisa = soup.select('li.f-bd')
    # lisa = soup.select('ul.f-hide')
    # print(lisa)
    play_list = []
    for li in lisa:
        song_id = li.find('a', attrs={'data-res-type': 'song'})['data-res-id']
        title = li.h3.get_text()      #<h3 class="s-fc1 f-thide">阴天快乐</h3>
        img_url = song_img(song_id)
        url = song_url(song_id)
        # print(title, url, img_url)
        print('in here')
        play_list.append({'title': title, 'url': url, 'img_url': img_url})

        # a = Album(d)
        # a.nusicfm_id = 1  # 1 代表 doubanFM
        # a.save()
    album_id = album.get('album_id')
    print('out here', album_id)
    for pl in play_list:
        print('pl', pl)
        p = Playlist(pl)
        p.album_id = album_id
        print('save playlist', album_id)
        p.save()

    # print(play_list)
    return play_list



# b = os.urandom(1)
# a = ord(b)
# print(a)
def neteasy_spider():
    album = top_playlist()
    # print(album)
    for l in album:
        playlist_detail(l)

if __name__ == '__main__':
    neteasy_spider()