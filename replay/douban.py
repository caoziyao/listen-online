
from replay import *


from models.play import Album
from models.play import Playlist

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


def get_album():
    urls = ['https://douban.fm/j/v2/songlist/explore?type=hot&genre={}'.format(i) for i in range(0, 18) ]
    # print(urls)
    playlist = []
    for url in urls:
        data = json.loads(_db_h(url))
        time.sleep(0.5)
        for d in data:
            # description = d.get('description')
            title = d.get('title')
            cover_img_url = d.get('cover')
            album_id = d.get('id')
            url = 'https://douban.fm/j/v2/songlist/{}/?kbps=192'.format(album_id)

            playlist.append({'title': title, 'cover_img_url': cover_img_url, 'url': url, 'album_id': album_id})
            print('save album ', title, cover_img_url)
            get_playlist(url, album_id)
    return playlist

# playlist
# [{'title': title, 'cover_img_url': cover_img_url, 'url': url}, {}, {}]
def spider_fm():
    """
    api
    """
    # urls = get_doubanfmUrl()
    # ids = [301715, 10767176, 1388497, 429077, 1342044, 8961784, 11805147, 260812]
    # ids = [368352, 10756490, 306878, 7925757,  287050, 450370, 9714644, 260086, 1298891, 287050, 6595891, 485660, 5521949]

    pls = get_playlist()

    for p in pls:
        url = p.get('url')
        album_id = p.get('album_id')
        # url = 'https://douban.fm/j/v2/songlist/{}/?kbps=192'.format(id)
        get_playlist(url, album_id)
        time.sleep(1)


def get_playlist(url, album_id):
    # id 443635  10416548
    # playlist_id = 10416548
    # playlist_id = 306878 #7925757  #287050  #450370 #9714644  # 260086
    # url = 'https://douban.fm/j/v2/songlist/{}/?kbps=192'.format(playlist_id)
    print(url)

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
        # print(song)
        result.append(_convert_song2(song))

    # d = dict(playlist=result, album=album)
    
    a = Album(album)
    a.nusicfm_id = 1    # 1 代表 doubanFM
    a.save()

    for pl in result:
        p = Playlist(pl)
        p.album_id = a.id
        p.save()
    return None     # 因为保存到数据库中了，不需要在返回
    
