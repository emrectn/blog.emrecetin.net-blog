from app.models import DBSession, User, Article


def get_user(token):
    db = DBSession()
    user = db.query(User).filter(User.token == token).first()

    if user:
        data = user.to_dict()
    else:
        data = None
    db.close()
    return data


def get_user_with_credentials(email, password):
    db = DBSession()
    u = db.query(User).filter(User.email == email,
                              User.password == password).first()

    if u:
        data = u.to_dict()
    else:
        data = None
    db.close()
    return data


def login(email, password):

    db = DBSession()
    u = db.query(User).filter(User.email == email,
                              User.password == password).first()
    token = None
    if u and (u.status == 0):
        print("içerdema ")
        token = u.update_token()
        print(token)
        db.commit()
    db.close()

    if not u:
        print("Gecersiz kullanici")
        return None
    return token


def is_admin(token):
    user = get_user(token)
    if user['rank'] == 0:
        return True
    print('Admin Degil')
    return False


def is_authorized(token, post_id):
    status = is_admin(token)
    if status:
        return True

    user = get_user(token)

    db = DBSession()
    status = db.query(Article).filter(Article.user_id == user['id'],
                                      Article.id == post_id).first()
    db.close()

    if status:
        return True

    print("Yetkili Degil veya Post yok")
    return False


def create_user(email, password, fullname, userinfo="..."):
    db = DBSession()
    user = User(email=email,
                password=password,
                fullname=fullname,
                userinfo=userinfo)
    db.add(user)
    db.commit()
    data = user.to_dict()
    db.close()
    return data


def inactive_user(user_id):
    db = DBSession()
    user = db.query(User).get(user_id)
    if user:
        user.status = 3
        db.commit()
        db.close()
        return user.status
    return None


def change_password(user_id, new_password, old_password):
    db = DBSession()
    user = db.query(User).get(user_id)

    if user and user.password == old_password:
        user.password = new_password
        db.commit()
        data = user.to_dict()
        db.close()
        return data
    print("Gecersiz kullanıcı adı veya token")
    return None
