from flask_restful import Resource, fields, marshal_with
from .api import api
from ..models import Post

field = {
	'id':fields.Integer,
	'body':fields.String,
	'timestamp':fields.String,
	'url': fields.Url('api.foo', absolute=True),
	'comment_count': fields.Integer
}

class Test:
	def __init__(self, id, name):
		self.id = id
		self.name = name

test = Test(1, 'john')

class Foo(Resource):
	@marshal_with(field)
	def get(self):
		post =  Post.query.get_or_404(6)
		post.comment_count = 5
		return post
