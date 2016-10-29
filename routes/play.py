from models.play import Playlist
from routes import *

from replay.douban import spider_fm

from models.play import Album
from models.play import Playlist
from models.play import MusicFM

main = Blueprint('play', __name__)
save_albumid = 368352



def get_albumlist(page, als):
    """
    返回页面列表
    """
    start = page * 8 - 8
    end = page * 8 
    l = als[start:end]
    return l

@main.route('/index/<int:page>/fmid/<int:fmid>')        # 翻页
@main.route('/index/<int:page>/fmid/<int:fmid>/play/<int:album_id>', methods=['GET'])   # 播放
def play(album_id=None, page=1, fmid=1):
    global save_albumid

    # 所有专辑
    if album_id is not None:
        id = int(album_id)
        save_albumid = id
        al = Album.query.filter_by(album_id=id).first()
    else:
        al = Album.query.filter_by(album_id=save_albumid).first()

    als = MusicFM.query.get(fmid).album
    # als = Album.query.all()
    pl = al.playlist
    
    l = get_albumlist(page, als)

    total = len(als) // 8 + 1
    p = dict(
        total = total,
        page = page,
    )
    return render_template('play.html', albums=l, playlists=pl, page=p, fmid=fmid)



@main.route('/')
@main.route('/fmid/<int:fmid>')
def index(page=1, fmid=1):
    # 10416548
    # spider_fm()
    print(fmid)


    # 所有专辑
    als = MusicFM.query.get(fmid).album
    # als = Album.query.all()
    total = len(als) // 8 + 1
    p = dict(
        total = total,
        page = page,
    )

    l = get_albumlist(page, als)

    # 默认播放第一个
    pl = als[0].playlist
    return render_template('play.html', albums=l, playlists=pl, page=p, fmid=fmid)

# @main.route('/index/<int:page>')
# def turning(page=1):
#     global save_albumid
#     # 10416548
#     # get_playlist()

#     als = Album.query.all()
#     # print('al', als)
    
#     total = len(als) // 8 + 1

#     # 分页链接会自动添加p这个参数，表示页码
#     start = page * 8 - 8
#     end = page * 8 
#     list_al = als[start:end]

#     al = Album.query.filter_by(album_id=save_albumid).first()
#     # print('al', al)
#     pl = al.playlist
#     p = dict(
#         total = total,
#         page = page,
#     )

#     return render_template('play.html', albums=list_al, playlists=pl, page=p)

