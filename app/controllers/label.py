from app.models import DBSession, Label, ArticleLabel


def get_label(label_name):
    db = DBSession()
    data = db.query(Label).filter(Label.name == label_name).first()

    if data:
        return data
    return None


def create_label(label_name):
    db = DBSession()
    print('yeni label : {}'.format(label_name))
    p = Label(name=label_name)
    db.add(p)
    db.commit()
    db.close()
    return


def get_or_create_label(label_name):

    data = get_label(label_name)
    if data:
        print("Bulundu")
        return data.id

    create_label(label_name)

    data = get_label(label_name)
    if data:
        return data.id
    return None


def add_label(data, post_id):

        label_id = get_or_create_label(data)
        add_label_article(label_id, post_id)
        return label_id


def get_label_article(label_id, post_id):
    db = DBSession()
    data = db.query(ArticleLabel).filter(ArticleLabel.label_id == label_id,
                                         ArticleLabel.post_id == post_id).first()

    if data:
        return data.id
    return None


def create_label_article(label_id, post_id):
    db = DBSession()
    p = ArticleLabel(label_id=label_id, post_id=post_id)
    db.add(p)
    db.commit()
    db.close
    return


def add_label_article(label_id, post_id):
    status = get_label_article(label_id, post_id)
    if not status:
        create_label_article(label_id, post_id)


def delete_label(label_id):
    db = DBSession()
    data = db.query(Label).get(label_id)
    db.delete(data)
    db.commit()
    db.close
    return {'status': 'OK'}
