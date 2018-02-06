from config import DB_URI
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.types import DateTime
from sqlalchemy import create_engine
from uuid import uuid4
from time import time

from enum import Enum
import hashlib

Base = declarative_base()


class UserStatus(Enum):
    ACTIVE = 0
    INACTIVE = 1
    BANNED = 2
    DELETED = 3


class UserRank(Enum):
    ADMIN = 0
    EDITOR = 1
    USER = 2


class Publish(Enum):
    ON_AIR = 0
    NOT_ON_AIR = 1


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(50), nullable=False)
    email = Column(String(50), unique=True)
    password = Column(String(50), nullable=False)
    userinfo = Column(String(250))
    status = Column(Integer, default=UserStatus.INACTIVE.value, nullable=False)
    rank = Column(Integer, default=UserRank.USER.value, nullable=False)
    token = Column(String(250))
    token_gen_time = Column(Integer)

    def __repr__(self):
        return '<User(id: {}, email: \'{}\'>'.format(self.id, self.email)

    def update_token(self):
        token = str(uuid4())
        # m = hashlib.sha256()
        # username_token = m.update(b"{}".format(self.asdemail)).hexdigest()
        self.token = token
        self.token_gen_time = int(time())
        return token

    def to_dict(self):
        return {
            'id': self.id,
            'fullname': self.fullname,
            'email': self.email,
            'password': self.password,
            'userinfo': self.userinfo,
            'status': self.status,
            'rank': self.rank,
            'token': self.token,
            'token_gen_time': self.token_gen_time
        }


class ArticleLabel(Base):
    """docstring for Comment"""
    __tablename__ = 'articles_labels'
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey("articles.id", onupdate='CASCADE', ondelete='CASCADE'))
    label_id = Column(Integer, ForeignKey("labels.id", onupdate='CASCADE', ondelete='CASCADE'))

    def __repr__(self):
        return '<ArticleLabel(id: {}, label_id: {}>, article_id: {}'.format(
            self.id, self.label_id, self.article_id)


class Label(Base):
    """docstring for Label"""
    __tablename__ = 'labels'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    article_label = relationship(ArticleLabel, backref="label", passive_deletes=True)

    def __repr__(self):
        return '<Label(id: {}, labelName: {}>'.format(self.id, self.name)

    def to_dict(self):
        return {'id': self.id,
                'name': self.name}


class Comment(Base):
    """docstring for Comment"""
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    text = Column(String(200), nullable=False)
    date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    article_id = Column(Integer, ForeignKey('articles.id', onupdate='CASCADE', ondelete='CASCADE'))
    likes = Column(Integer, default=0)
    unlikes = Column(Integer, default=0)
    publish = Column(Integer, default=Publish.ON_AIR.value)

    def __repr__(self):
        return '<Comment(id: {}, text: {}>'.format(
            self.id, self.text)

    def to_dict(self):
        return {'id': self.id,
                'text': self.text,
                'date': str(self.date),
                'user_id': self.user_id,
                'article_id': self.article_id,
                'likes': self.likes,
                'unlikes': self.unlikes,
                'publish': self.publish}


class Article(Base):
    """docstring for Article"""
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    text = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    image = Column(String, default='/static/0.jpg')
    seen = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    unlikes = Column(Integer, default=0)
    publish = Column(Integer, nullable=False, default=Publish.ON_AIR.value)
    user_id = Column(Integer, ForeignKey('users.id'))
    # relationship Join yapmaya yarar.
    article_label = relationship(ArticleLabel, backref="article", passive_deletes=True)
    comment = relationship(Comment, backref="comments", passive_deletes=True)
    user = relationship('User')

    # Geri döndürğümüz format
    def __repr__(self):
        return '<Article(id: {}, title: {}, writer: {}>'.format(
            self.id, self.title, self.user_id)

    # dictionary  çevirmeye yarıyor
    def to_dict(self):
        return {'id': self.id,
                'title': self.title,
                'text': self.text,
                'date': str(self.date),
                'image': self.image,
                'seen': self.seen,
                'likes': self.likes,
                'unlikes': self.unlikes,
                # user relationshipte user ile bağlantı sağlanır.
                'author': self.user.fullname}


# local veritabanı
engine = create_engine(DB_URI)

# tablolar veritabanına kaydedildi.
Base.metadata.create_all(engine)

# Database session oluşturucu oluşturuldu
DBSession = sessionmaker(engine)
