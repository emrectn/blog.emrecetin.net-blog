from app.models import DBSession, Article


def get_post(post_id):
    db = DBSession()
    data = db.query(Article).get(post_id)
    if data:
        data = data.to_dict()
    db.close()
    return data


def delete_post(post_id):
    db = DBSession()
    data = db.query(Article).get(post_id)
    if data and data.publish == 0:
        db.delete(data)
        db.commit()
        db.close()
        return {'status': 'OK'}
    db.close()
    return None


def get_posts():
    db = DBSession()
    all_posts = db.query(Article)
    db.close()
    return [p.to_dict() for p in all_posts]


def add_post(title, text, date, user_id, image="/static/0.jpg"):
    db = DBSession()
    # eger keyword arguman olarak eklmessek, veritabanında eslesme olmayacagı
    # icin hata alınır.
    p = Article(title=title,
                text=text,
                date=date,
                user_id=user_id,
                image=image)
    db.add(p)
    db.commit()
    db.close()
    return True
