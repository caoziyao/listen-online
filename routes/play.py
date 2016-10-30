from models.play import Playlist
from routes import *

from replay.douban import spider_fm
from replay.netease import neteasy_spider

from models.play import Album
from models.play import Playlist
from models.play import MusicFM

main = Blueprint('play', __name__)
save_albumid = 368352


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
    spider_task()
    # return redirect(url_for('play.index'))
    return 'hello'

def spider_task():
    """
    多线程爬虫
    """
    # spider_fm()
    neteasy_spider()

    # starttime = time.time()  # 记录开始时间
    # threads = []  # 创建一个线程列表，用于存放需要执行的子线程
    # t1 = threading.Thread(target=neteasy_spider)  # 创建第一个子线程，子线程的任务是调用task1函数，注意函数名后不能有（）
    # threads.append(t1)  # 将这个子线程添加到线程列表中
    # for t in threads:  # 遍历线程列表
    #     t.setDaemon(True)  # 将线程声明为守护线程，必须在start() 方法调用之前设置，如果不设置为守护线程程序会被无限挂起
    #     t.start()  # 启动子线程
    # endtime = time.time();  # 记录程序结束时间
    # totaltime = endtime - starttime;  # 计算程序执行耗时
    # print("耗时：{0:.5f}秒".format(totaltime));  # 格式输出耗时