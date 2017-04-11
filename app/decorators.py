from functools import wraps

from flask_login import current_user
from flask import abort

from .models import Permission

def permission_required(permission):
	def decorator(f):
		@wraps(f)
		def decorated_f(*args, **kws):
			if not current_user.can(permission):
				abort(403)
			return f(*args, **kws)
		return decorated_f
	return decorator

def admin_required(f):
	return permission_required(Permission.ADMINISTER)(f)