from flask import g, abort

from functools import wraps


def permission_required(permission):
	def decorator(f):
		wraps(f)
		def _(*args, **kws):
			if not g.current_user.can(permission):
				abort(403)
			return f(*args, **kws)
		return _
	return decorator