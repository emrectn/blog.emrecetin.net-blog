from app.models import DBSession, User, UserArticle


def get_user(token):
    db = DBSession()
    user = db.query(User).get(token)
    db.close()

    if not user:
        return None
    return user.to_dict()


def get_user_without_token(email, password):
    db = DBSession()
    u = db.query(User).filter(User.email == email,
                              User.password == password).first()
    if u:
        return u.to_dict
    return None


def login(email, password):
    db = DBSession()
    u = db.query(User).filter(User.email == email,
                              User.password == password).first()

    if u and (u.status == 0 or u.status == 1):
        token = u.update_token()
        db.commit()
    db.close()

    if not u:
        return None
    return token


def is_admin(token):
    user = get_user(token)
    if user['permission'] == 0:
        return True
    return False


def is_authorized(token, post_id):
    status = is_admin(token)
    if status:
        return True

    user = get_user(token)
    db = DBSession()
    user = db.query(UserArticle).filter(UserArticle.user_id == user[id],
                                        UserArticle.post_id == post_id).first()
    if user:
        return True
    return False


def create_user(email, password, fullname, userinfo="..."):
    db = DBSession()
    user = User(email=email,
                password=password,
                fullname=fullname,
                userinfo=userinfo)
    db.add(user)
    db.commit()
    db.close
    return user.to_dict()


def inactive_user(user_id):
    db = DBSession()
    user = db.query(User).get(user_id)
    if user:
        user.status = 3
        db.commit()
        db.close
        return user.status
    return None


def change_password(user_id, password):
    db = DBSession()
    user = db.query(User).get(user_id)
    if user:
        user.password = password
        db.commit()
        db.close
        return user.to_dict()
    return None
