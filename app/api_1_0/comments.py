from .api import api
from ..models import Comment

from flask_restful import Resource, marshal, marshal_with, fields

comment_field = {
	'url': fields.Url('api.comments', absolute=True)
}

comments_field = {
	'comments': fields.List(fields.Nested(comment_field))
}
class PostComments(Resource):
	pass

class Comments(Resource):
	def get(self, id=None):
		if id is None:
			return marshal({'comments': Comment.query.all()}, comments_field)
		return marshal(Comment.query.get_or_404(id), comment_field)