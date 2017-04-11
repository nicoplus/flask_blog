
from .. import  admin_instance,db
from ..models import User, Post
from ..decorators import admin_required

from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.base import MenuLink
from flask_login import current_user
from flask import redirect, url_for

import os

class MyModelView(ModelView):
	column_exclude_list=['password_hash',]
	can_view_details = True

	def is_accessible(self):
		return current_user.is_administrator()




admin_instance.add_view(FileAdmin('./app/static', '/static/', name='Static Files'))
admin_instance.add_view(MyModelView(User, db.session))
admin_instance.add_view(MyModelView(Post, db.session))
admin_instance.add_link(MenuLink(name='Back Client', url='/'))

