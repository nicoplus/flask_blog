from flask_httpauth import HTTPBasicAuth
from flask import g
from flask_restful import Resource

from ..models import AnonymousUser,User
from .errors import unauthorized, forbidden
from . import api_blueprint
from .api import api

auth  = HTTPBasicAuth()

@auth.verify_password
def verify_password(email_or_token, password):
	if email_or_token == '':
		g.current_user = AnonymousUser()
		return True
	if password == '':
		g.current_user = User.verify_auth_token(email_or_token)
		g.token_used = True
		return g.current_user is not True
	user = User.query.filter_by(email=email_or_token).first()
	if not user:
		return False
	g.current_user = user
	g.token_used = False
	return user.verify_password(password)

@auth.error_handler
def auth_error():
	return unauthorized('Invalid credentials')

@api_blueprint.before_request
@auth.login_required
def before_request():
	if not g.current_user.is_anonymous and not g.current_user.confirmed:
		return forbidden('Unconfirmed account')


class TokenResource(Resource):
	def get(self):
		if g.current_user.is_anonymous or g.token_used:
			return unauthorized('Invalid credentials')
		return {'token': g.current_user.generate_auth_token(3600), 
				'expiration': 3600}


api.add_resource(TokenResource, '/token/')

