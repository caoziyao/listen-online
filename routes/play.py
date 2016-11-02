from models.play import Playlist
from routes import *

from replay.douban import douban_master
from replay.netease import neteasy_spider
from replay.qqmusic import qqmusic_fm

from models.play import Album
from models.play import Playlist
from models.play import MusicFM

main = Blueprint('play', __name__)
save_albumid = 1


def get_albumlist(page, als):
    """
    返回页面列表
    每页 8 个专辑
    """
    start = page * 8 - 8
    end = page * 8 
    l = als[start:end]
    return l


@main.route('/index/<int:page>/fmid/<int:fmid>')        # 翻页
@main.route('/index/<int:page>/fmid/<int:fmid>/play/<int:album_id>', methods=['GET'])   # 播放
def play(album_id=None, page=1, fmid=1):
    """
    album_id: 专辑id
    playlist: 每张专辑若干歌曲
    page: 页面数 每页 8 个专辑
    fmid: 如doubanFM=1， netease=2 qq=3
    """
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
    # pl = al.playlist
    pl = als[0].playlist

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
    """
    album_id: 专辑id
    playlist: 每张专辑若干歌曲
    page: 页面数 每页 8 个专辑
    fmid: 如doubanFM=1， netease=2 qq=3
    """
    # print(fmid)

    # 所有专辑
    als = MusicFM.query.get(fmid).album
    # als = Album.query.all()
    total = len(als) // 8 + 1
    p = dict(
        total = total,
        page = page,
    )
    # 每页 8 个专辑
    l = get_albumlist(page, als)

    # 默认播放第一个
    index = randrange(0, len(als))
    pl = als[index].playlist
    return render_template('play.html', albums=l, playlists=pl, page=p, fmid=fmid)


@main.route('/spider')
def spider():
    """
    爬取数据
    :return:
    """
    # douban_fm()
    qqmusic_fm()
    # return redirect(url_for('play.index'))
    return 'hello'



