from flask import g
from flask_restful import fields, Resource, marshal_with, reqparse

from ..models import User

OneUserField = {
	'url': fields.Url('api.one_user', absolute=True),
	'username': fields.String,
	'member_since':fields.DateTime,
	'last_seen':fields.DateTime,
	'posts':fields.Url('api.user_posts', absolute=True),
	'followed_posts':fields.Url('api.user_timeline', absolute=True),
	'post_count':fields.Integer
}

class OneUser(Resource):
	@marshal_with(OneUserField)
	def get(self, id):
		user = User.query.get_or_404(id)
		user.post_count = user.posts.count()
		return user