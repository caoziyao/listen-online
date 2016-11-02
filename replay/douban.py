


from replay import *

import queue


# 歌曲榜单地址
top_list_all = {
    1: ['流行', 'https://douban.fm/j/v2/songlist/explore?type=hot&genre=1'],
}

def json_save(data):
    """
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    path = os.path.join( os.getcwd(), 'models/playlist.txt')
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(s)

def json_load():
    path = os.path.join( os.getcwd(), 'models/playlist.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return json.loads(s)


def _db_h(url):
    """
    爬取网页信息
    """
    data = requests.get(url)
    data = data.text

    return data

def _convert_song2(song):
    album_title = song.get('albumtitle')
    if album_title is None:
        album_title = ''
    d = {
        'id': 'dbtrack_' + str(song['sid']),
        'title': song['title'],
        'artist': song['singers'][0]['name'],
        'artist_id': 'dbartist_' + song['singers'][0]['id'],
        'album': album_title,
        'album_id': 'dbalbum_' + song['aid'],
        'img_url': song['picture'],
        'url': song['url'],
        'source': 'douban',
        'source_url': 'https://music.douban.com/subject/%s/'.format(song['aid']),
    }
    return d


def parsed_playlist(url, album_id):
    # print(url)
    time.sleep(0.5)
    # 获取网页信息
    # 豆瓣fm 的事 json 格式
    data = json.loads(_db_h(url))

    album = dict(
        cover_img_url = data['cover'],
        title = data['title'],
        album_id = album_id,
    )
    result = []
    for song in data['songs']:
        result.append(_convert_song2(song))

    a = Album(album)
    a.nusicfm_id = 1    # 1 代表 doubanFM
    a.save()

    for pl in result:
        p = Playlist(pl)
        p.album_id = a.id
        p.save()
    return None     # 因为保存到数据库中了，不需要在返回


def parsed_album(url):
    data = json.loads(_db_h(url))
    for d in data:
        # description = d.get('description')
        title = d.get('title')
        cover_img_url = d.get('cover')
        album_id = d.get('id')
        url = 'https://douban.fm/j/v2/songlist/{}/?kbps=192'.format(album_id)

        # playlist.append({'title': title, 'cover_img_url': cover_img_url, 'url': url, 'album_id': album_id})
        print('save album ', title, cover_img_url)
        parsed_playlist(url, album_id)
    

#----------------api--------------
def store(url):
    time.sleep(1)
    parsed_album(url)

"""
如果我们能把这个queue放到这台master机器上，所有的slave都可以通过网络跟master联通，
每当一个slave完成下载一个网页，就向master请求一个新的网页来抓取。
而每次slave新抓到一个网页，就把这个网页上所有的链接送到master的queue里去
链接：https://www.zhihu.com/question/20899988/answer/24923424
"""
# [{'title': title, 'cover_img_url': cover_img_url, 'url': url}, {}, {}]
request = queue.Queue()

def send(url):
    request.put(url)


def request_from_master():
    return request.get()


def douban_slave(url):
    # current_url = request_from_master()
    current_url = url
    print(current_url)
    # 把这个url代表的网页存储好
    store(current_url)



def douban_master():
    urls = ['https://douban.fm/j/v2/songlist/explore?type=hot&genre={}'.format(i) for i in range(10, 18) ]
    
    url_queue = queue.Queue()
    for url in urls:
        url_queue.put(url)

    while True:
        if not url_queue.empty():
            douban_slave(url_queue.get())
        else:
            break

# douban_master()
        # url = p.get('url')
        # album_id = p.get('album_id')
        # # url = 'https://douban.fm/j/v2/songlist/{}/?kbps=192'.format(id)
        # get_playlist(url, album_id)
        # time.sleep(1)
