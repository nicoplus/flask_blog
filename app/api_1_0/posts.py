from flask_restful import Resource, fields, marshal_with, marshal, reqparse
from flask import url_for, g
from .. import db

from ..models import User, Post, Permission
from .api import api
from decorators import permission_required

class UrlForFiled(fields.Raw):
	def format(self, value):
		return url_for('api.one_user', id=value)

class CountField(fields.Raw):
	def format(self, value):
		return value.count()

post_field = {
	'url': fields.Url('api.posts', absolute=True),
	'author':UrlForFiled(attribute='author_id'),
	'body':fields.String,
	'body_html': fields.String,
	'timestamp':fields.DateTime,
	'comments': fields.Url('api.post_comments', absolute=True),
	'comment_count': CountField(attribute='comments')
}

posts_field = {
	'posts': fields.List(fields.Nested(post_field))
}

class Posts(Resource):
	def __init__(self):
		self.reqparser = reqparse.RequestParser()
		self.reqparser.add_argument('body', type=str, required=True, help="body can't be empty", location='json')

	def get(self, id=None):
		if id is None:
			return marshal({'posts':Post.query.all()}, posts_field)
		return marshal(Post.query.get_or_404(id), post_field)

	@permission_required(Permission.WRITE_ARTICLE)
	@marshal_with(post_field)
	def post(self):
		post = Post(author=g.current_user, body=self.reqparser.parse_args()['body'].decode('utf-8'))
		db.session.add(post)
		db.session.commit()
		return post, 201, {'Location':url_for('api.posts', id=post.id)}

class UserPosts(Resource):
	@marshal_with(posts_field)
	def get(self, id):
		posts = User.query.get_or_404(id).posts.all()
		return {'posts':posts}

class UserTimeLine(Resource):
	def get(self, id):
		pass

