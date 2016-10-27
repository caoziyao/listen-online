import time

from . import ModelMixin
from . import db


class Playlist(db.Model, ModelMixin):
    __tablename__ = 'playlists'
    id = db.Column(db.Integer, primary_key=True)
    cover_img_url = db.Column(db.String())
    title = db.Column(db.String())
    play_count = db.Column(db.Integer)

    # 这是一个外键
    # user_id = db.Column(db.Integer, db.ForeignKey('stb_users.id'))
    # # relationship
    # reviews = db.relationship('Review', backref='chest')

    def __init__(self, form):
        print('chest init', form)
        self.cover_img_url = ''
        self.title = ''
        self.play_count = 0

