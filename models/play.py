import time

from . import ModelMixin
from . import db


# class Playlist(object):
#     """
#     播放列表
#     """
#     def __init__(self):
#         self.cover_img_url = ''
#         self.title = ''
#         self.play_count = 0

class MusicFM(db.Model, ModelMixin):
    """
    1 doubanFM
    2 NetEasey
    """
    __tablename__ = 'musicfms'
    id = db.Column(db.Integer, primary_key=True)
    

class Album(db.Model, ModelMixin):
    """
    专辑
    """
    __tablename__ = 'albums'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    cover_img_url = db.Column(db.String())
    album_id = db.Column(db.Integer)

    # 这里要定义外键
    nusicfm_id = db.Column(db.Integer, db.ForeignKey('musicfms.id'))

    # 定义一个关系
    # foreign_keys 有时候可以省略, 比如现在...
    playlist = db.relationship('Playlist', backref='album')

    def __init__(self, d):
        self.title = d.get('album').get('title')
        self.cover_img_url = d.get('album').get('cover_img_url')
        self.album_id = d.get('album').get('album_id')

class Playlist(db.Model, ModelMixin):
    """
    播放列表
    """
    __tablename__ = 'playlists'
    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String())
    title = db.Column(db.String())
    url = db.Column(db.String())

    # 这是一个外键
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))
    # relationship
    # reviews = db.relationship('Review', backref='chest')

    def __init__(self, l):
        # print('chest init', form)

        self.img_url = l.get('img_url')
        self.title = l.get('title')
        self.url = l.get('url')

