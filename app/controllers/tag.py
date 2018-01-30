from app.models import DBSession, Label, ArticleLabel


def get_labels():
    db = DBSession()
    all_labels = db.query(Label)
    db.close()

    return [p.to_dict() for p in all_labels]


def get_label(label_id):
    db = DBSession()
    data = db.query(Label).get(label_id)
    if data:
        data = data.to_dict()
    db.close()
    return data