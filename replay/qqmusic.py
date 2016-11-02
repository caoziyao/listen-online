from bs4 import BeautifulSoup
from flask import url_for
from flask import Flask


# from multiprocessing import Process     #, Queue
import queue
import threading

from replay import *
from replay.replay import *

from bs4 import BeautifulSoup
from flask import url_for
from flask import Flask
from models.play import Album
from models.play import Playlist



r = queue.Queue(maxsize = 1000)




def _get_qqtoken():
    token_url = 'http://base.music.qq.com/fcgi-bin/fcg_musicexpress.fcg?' + \
        'json=3&guid=780782017&g_tk=938407465&loginUin=0&hostUin=0&' + \
        'format=jsonp&inCharset=GB2312&outCharset=GB2312&notice=0&' + \
        'platform=yqq&jsonpCallback=jsonCallback&needNewCode=0'
    jc = h(token_url)[len("jsonCallback("):-len(");")]
    return json.loads(jc)["key"]


def get_url_by_id(qqsid):
    token = _get_qqtoken()
    url = 'http://cc.stream.qqmusic.qq.com/C200%s.m4a?vkey=%s' + \
        '&fromtag=0&guid=780782017'
    song_url = url % (qqsid, token)
    return song_url


def get_img(url):
    web_data = requests.get(url).text
    soup = BeautifulSoup(web_data, 'lxml')
    try:
        img = 'http:' + soup.select('img.data__photo')[0]['src']
    except:
        img = ''
    return img


def parsed_playlist(album_id):
    """
    解析歌曲列表页面
    """
    time.sleep(1)
    host = 'http://y.qq.com/portal/album/{}.html'
    url = host.format(album_id)

    print('playlist', url)
    web_data = requests.get(url).text
    soup = BeautifulSoup(web_data, 'lxml')
    cover_img_url = 'http:' + soup.find(id = 'albumImg')['src']
    title = soup.select('h1.data__name_txt')[0]['title']

    album = dict(
        cover_img_url = cover_img_url,
        title = title,
        album_id = '',
    )
    a = Album(album)
    a.nusicfm_id = 3  # 3 代表 qq
    a.save()

    urls = soup.select('span.songlist__songname_txt a')
    for ur in urls:
        time.sleep(0.2)
        url = 'http:' + ur['href']
        img_url = get_img(url)

        qqsid = url.split('/song/')[1].split('.html')[0]
        url = get_url_by_id(qqsid)
        print(url)
        title = ur.get_text()


        p = Playlist({'url':url, 'title':title, 'img_url':img_url})
        p.album_id = a.id
        p.save()

    # print(title, cover_img_url)

def parsed_album(url):
    """
    解析专辑页面
    """
    print('album', url)
    host = 'http://y.qq.com/portal/album/{}.html'
    web_data = requests.get(url).text
    data = web_data.split('GetAlbumListJsonCallback')[1]
    # soup = BeautifulSoup(web_data.text, 'lxml')
    data = json.loads(data[len('('):-len(')')])

    albumlist = data['data']['albumlist']
    for al in albumlist:
        title=al.get('album_name', '')
        album_id=al.get('album_mid', '')

        url = host.format(album_id)
        parsed_playlist(album_id)
        # send({'url': url, 'parsed': 'playlist'})
        # print('save to r')

#----------------api--------------
def store(request):

    url = request.get('url', '')
    parsed = request.get('parsed', '')
    if parsed == 'album':
        parsed_album(url)
    # elif parsed == 'playlist':
    #     parsed_playlist(url)

"""
如果我们能把这个queue放到这台master机器上，所有的slave都可以通过网络跟master联通，
每当一个slave完成下载一个网页，就向master请求一个新的网页来抓取。
而每次slave新抓到一个网页，就把这个网页上所有的链接送到master的queue里去
链接：https://www.zhihu.com/question/20899988/answer/24923424
"""
# [{'title': title, 'cover_img_url': cover_img_url, 'url': url}, {}, {}]

def send(dic):
    r.put(dic)

def request_from_master():
    return r.get()


def qq_slave():
    time.sleep(1)
    while True:
        time.sleep(1)
        if not r.empty():
            req = request_from_master()
            store(req)
        else:
            break


def qq_master():
    q = queue.Queue()

    urls = ['http://c.y.qq.com/v8/fcg-bin/album_library?' + 
            'g_tk=938407465&jsonpCallback=GetAlbumListJsonCallback&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-' +
            '8&notice=0&platform=yqq&needNewCode=0&cmd=get_album_info&page={}&pagesize=20&sort=1&language=-1&genre=0&year=1&pay=0&type=-1&company=-1'.format(i) for i in range(3, 10) ]

    for url in urls:
        q.put({'url':url, 'parsed':'album'})
        

    while True:
        # print('1')
        if not q.empty():
            send(q.get())
            time.sleep(0.1)
        else:
            break


def qqmusic_fm():
    qq_master()
    qq_slave()



if __name__ == '__main__':
    # qqmusic_fm()
    url = 'http://y.qq.com/portal/song/001d7m7V0LPTyn.html'
    qqsid = url.split('/song/')
    print(qqsid)

# def qqmusic_fm():
#     qw = threading.Thread(target=qq_slave, name='slave')
#     qr = threading.Thread(target=qq_master, name='master')
#
#     qw.start()
#     qr.start()
#     qr.join()
#     qw.join()
#     print('end fm')


# def qqmusic_fm():
#     pw = Process(target=qq_master, args=('master', ))
#     pr = Process(target=qq_slave, args=('slave', ))

#     pw.start()
#     pr.start()
#     pw.join()
#     pr.join()
#     # pr.terminate()
#     print('child end')

