from flask_restful import Api, Resource

from . import api_blueprint



api = Api(api_blueprint, prefix='/api/v1.0')

from .resources import Foo
api.add_resource(Foo, '/foo/')

from .users import OneUser
api.add_resource(OneUser,'/users/<int:id>', endpoint='one_user')

from .posts import UserPosts, UserTimeLine, Posts
api.add_resource(UserPosts, '/users/<int:id>/posts', endpoint='user_posts')
api.add_resource(UserTimeLine, '/users/<int:id>/timeline', endpoint='user_timeline')
api.add_resource(Posts, '/posts/', '/posts/<int:id>' )


from .comments import PostComments, Comments
api.add_resource(PostComments, '/posts/<int:id>/comments', endpoint='post_comments')
api.add_resource(Comments, '/comments/<int:id>', '/comments')