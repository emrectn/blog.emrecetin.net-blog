from flask_admin.contrib.sqla import ModelView
from app.models import DBSession, User, Article, ArticleTag, Comment, Tag

admin_session = DBSession()
ModelView.create_modal = True
ModelView.edit_modal = True