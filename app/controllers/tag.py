from app.models import DBSession, Tag, ArticleTag
from flask import abort


def get_tag(tag_name):
    db = DBSession()
    data = db.query(Tag).filter(Tag.name == tag_name).first()
    db.close()

    if data:
        return data
    return None


def create_tag(tag_name):
    db = DBSession()
    p = Tag(name=tag_name)
    db.add(p)
    db.commit()
    db.close()
    return


def get_or_create_tag(tag_name):

    data = get_tag(tag_name)
    if data:
        return data.id

    create_tag(tag_name)

    data = get_tag(tag_name)
    if data:
        return data.id
    return None


def add_tag(data, post_id):

        tag_id = get_or_create_tag(data)
        add_tag_article(tag_id, post_id)
        return tag_id


def add_tag_article(tag_id, post_id):
    status = get_tag_article(tag_id, post_id)
    if not status:
        create_tag_article(tag_id, post_id)
    else:
        print("Bu posta daha önce bu etiket eklenmiş")
        abort(403)


def get_tag_article(tag_id, post_id):
    db = DBSession()
    data = db.query(ArticleTag).filter(ArticleTag.tag_id == tag_id,
                                         ArticleTag.article_id == post_id).first()
    db.close()

    if data:
        return data.id
    return None


def create_tag_article(tag_id, post_id):
    db = DBSession()
    p = ArticleTag(tag_id=tag_id, article_id=post_id)
    db.add(p)
    db.commit()
    db.close()
    return


def delete_tag(tag_id):
    db = DBSession()
    data = db.query(Tag).get(tag_id)
    db.delete(data)
    db.commit()
    db.close()
    return {'status': 'OK'}
