from app.models import DBSession, Article, Comment
from flask import abort
from sqlalchemy.exc import IntegrityError
from app.controllers.user import is_admin


def get_article_comments(post_id):
    db = DBSession()
    comments = db.query(Comment).filter(Comment.article_id == post_id)
    comments = [c.to_dict() for c in comments]
    db.close()
    return comments


def get_user_comments(user_id):
    db = DBSession()
    comments = db.query(Comment).filter(Comment.user_id == user_id)
    comments = [c.to_dict() for c in comments]
    db.close()
    return comments


def add_comment(text, date, user_id, post_id):
    db = DBSession()
    p = Comment(text=text,
                date=date,
                user_id=user_id,
                article_id=post_id)

    db.add(p)

    try:
        db.commit()
        status = True
    except IntegrityError:
        db.rollback()
        status = None
    db.close()
    return status


def delete_comment(comment_id):
    db = DBSession()
    data = db.query(Comment).get(comment_id)
    if data:
        db.delete(data)
        db.commit()
    db.close()
    return data


def is_owner(user_id, comment_id):
    db = DBSession()
    data = db.query(Comment).filter(Comment.id == comment_id and
                                    Comment.user_id == user_id).first()
    db.delete(data)
    db.commit()
    db.close()
    return True


def publish_comment(comment_id):
    db = DBSession()
    data = db.query(Comment).get(comment_id)
    data.publish = 1
    db.commit()
    db.close()
    return True
