from app.models import DBSession, Article, Comment
from flask import abort


def get_article_comments(post_id):
    db = DBSession()
    comments = db.query(Comment).filter(Comment.article_id == post_id).all()
    comments = comments.to_dict() if comments else None
    db.close()
    return comments


def add_comment(text, date, user_id, post_id):
    db = DBSession()
    p = Comment(text=text,
                date=date,
                user_id=user_id,
                article_id=post_id)

    db.add(p)
    db.commit()
    db.close()
    return True