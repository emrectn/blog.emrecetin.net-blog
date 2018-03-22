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


def get_posts(page, size):
    db = DBSession()
    all_posts = db.query(
        Article).order_by(Article.date.desc()).offset(page*size).limit(size)
    all_posts = [p.to_dict() for p in all_posts]
    db.close()
    return all_posts


def get_populars(size=5):
    db = DBSession()
    populars = db.query(Article).order_by(
        Article.likes.desc()).limit(size).from_self().order_by(Article.date.desc())
    populars = [p.to_dict() for p in populars]
    db.close()
    return populars


def add_post(title, text, date, user_id, image="/static/0.jpg", seen=0, likes=0):
    db = DBSession()
    # eger keyword arguman olarak eklmessek, veritabanında eslesme olmayacagı
    # icin hata alınır.
    p = Article(title=title,
                text=text,
                date=date,
                user_id=user_id,
                image=image,
                seen=seen,
                likes=likes)
    db.add(p)
    db.commit()
    db.close()
    return True
