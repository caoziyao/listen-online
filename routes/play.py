from models.play import Playlist
from routes import *

from replay.douban import get_playlist
from models.play import Album
from models.play import Playlist

main = Blueprint('play', __name__)


@main.route('/index/<int:page>/play/<int:album_id>', methods=['GET'])
def play(album_id, page=1):
    # 10416548
    # info = get_playlist()
    id = int(album_id)
    als = Album.query.all()
    al = Album.query.filter_by(album_id=id).first()
    # print('al', al)
    pl = al.playlist


    # print('al', als)
    total = len(als) // 8 + 1
    # 分页链接会自动添加p这个参数，表示页码
    start = page * 8 - 8
    end = page * 8 
    list_al = als[start:end]
    p = dict(
        total = total,
        page = page,
    )
    return render_template('play.html', albums=list_al, playlists=pl, page=p)



@main.route('/')
@main.route('/index/<int:page>')
def index(page=1):
    # 10416548
    # get_playlist()

    als = Album.query.all()
    # print('al', als)
    
    total = len(als) // 8 + 1

    # 分页链接会自动添加p这个参数，表示页码
    start = page * 8 - 8
    end = page * 8 
    list_al = als[start:end]

    pl = als[start].playlist
    p = dict(
        total = total,
        page = page,
    )

    return render_template('play.html', albums=list_al, playlists=pl, page=p)


