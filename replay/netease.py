from replay import *
from replay.replay import *

from flask import url_for
from flask import Flask

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

modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b72' + \
          '5152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbd' + \
          'a92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe48' + \
          '75d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
nonce = '0CoJUm6Qyw8W8jud'
pubKey = '010001'


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


def song_img(song_id):
    action = 'http://music.163.com/m/song/{}?autoplay=true'.format(song_id)
    header = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36'
    }
    data = requests.get(action, headers=header)
    soup = BeautifulSoup(data.text, 'lxml')
    # print(soup)
    # url = soup.find('img', attrs={"class": "j-img"})['src']
    url = soup.select('div.img img')[0]['src']
    # print(url)
    time.sleep(0.5)
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
    time.sleep(0.5)
    return url


# 歌单（网友精选碟） hot||new http://music.163.com/#/discover/playlist/
def top_playlist(category='流行', order='hot', offset=0, limit=50):
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
    print(divs)
    for div in divs:
        img_url = div.find('img', attrs={"class": "j-flag"})['src']
        title = div.find('a', attrs={'class': 'msk'})['title']
        url = host + div.find('a', attrs={'class': 'msk'})['href']
        album_id = div.find('a', attrs={'class': 'icon-play'})['data-res-id']
        album_id = int(album_id)

        d = {'title': title, 'cover_img_url': img_url, 'url': url, 'album_id': album_id}
        album.append(d)

        flag = False
        alivs = Album.query.filter_by(nusicfm_id=2).all()
        for als in alivs:
            if album_id == als.album_id:
                flag = True
                break
        if flag:
            continue


        # 保存到数据库中
        # for al in album:
        a = Album(d)
        a.nusicfm_id = 2    # 2 代表 doubanFM
        a.save()
        print('a.id', a.id)
        playlist_detail(d, a.id)
    # return album


# 歌单详情
def playlist_detail(album, id):
    """
    返回 歌单列表
    """
    # action = 'http://music.163.com/m/playlist?id=496240695'
    header = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36'
    }
    # action = 'http://music.163.com/#/playlist?id=496240695'
    # 变成 action = 'http://music.163.com/m/playlist?id=496240695'
    action = album.get('url').replace('#', 'm')
    print('geting from', action)
    # time.sleep(0.5)
    data = requests.get(action, headers=header)
    soup = BeautifulSoup(data.text, 'lxml')
    lisa = soup.select('li.f-bd')
    # lisa = soup.select('ul.f-hide')
    # print(lisa)
    play_list = []
    for li in lisa:
        song_id = li.find('a', attrs={'data-res-type': 'song'})['data-res-id']
        title = li.h3.get_text()
        img_url = song_img(song_id)
        url = song_url(song_id)
        print(title, url, img_url)
        d = {'title': title, 'url': url, 'img_url': img_url}
        play_list.append(d)

        # save db
        p = Playlist(d)
        p.album_id = id
        p.save()

    # print(play_list)
    # return play_list


# b = os.urandom(1)
# a = ord(b)
# print(a)
def neteasy_spider():
    # save album

    top_playlist()


if __name__ == '__main__':
    neteasy_spider()