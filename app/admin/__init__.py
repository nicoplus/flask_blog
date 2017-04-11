from flask_admin import AdminIndexView, expose
from ..decorators import admin_required
class MyAdminIndexView(AdminIndexView):

	@expose('/')
	@admin_required
	def index(self):
		return super(MyAdminIndexView, self).index()