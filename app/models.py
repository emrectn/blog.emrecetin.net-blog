from config import DB_URI
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.types import DateTime
from sqlalchemy import create_engine
from uuid import uuid4
from time import time

from enum import Enum

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
    publish = Column(Integer, nullable=False, default=Publish.ON_AIR.value)
    user_id = Column(Integer, ForeignKey('users.id'))
    # relationship Join yapmaya yarar.
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
                # user relationshipte user ile bağlantı sağlanır.
                'author': self.user.fullname}


class Label(Base):
    """docstring for Label"""
    __tablename__ = 'labels'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return '<Label(id: {}, labelName: {}>'.format(self.id, self.name)

    def to_dict(self):
        return {'id': self.id,
                'name': self.name}


class Commment(Base):
    """docstring for Commment"""
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    text = Column(String(200), nullable=False)
    date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    article_id = Column(Integer, ForeignKey('articles.id'))

    def __repr__(self):
        return '<Commment(id: {}, text: {}>'.format(
            self.id, self.text)


class ArticleLabel(Base):
    """docstring for Commment"""
    __tablename__ = 'articles_labels'
    id = Column(Integer, primary_key=True)
    label_id = Column(Integer, ForeignKey('labels.id'))
    article_id = Column(Integer, ForeignKey('articles.id'))

    def __repr__(self):
        return '<Commment(id: {}, label_id: {}>, article_id: {}'.format(
            self.id, self.label_id, self.article_id)


class UserArticle(Base):
    """docstring for UserArticle"""
    __tablename__ = 'users_articles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    article_id = Column(Integer, ForeignKey('articles.id'))


# local veritabanı
engine = create_engine(DB_URI)

# tablolar veritabanına kaydedildi.
Base.metadata.create_all(engine)

# Database session oluşturucu oluşturuldu
DBSession = sessionmaker(engine)
