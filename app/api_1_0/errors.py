from flask import jsonify

from ..exceptions import ValidationError
from . import api_blueprint

def forbidden(message):
	response = jsonify({'error':'forbidden', 'message':message})
	response.status_code = 403
	return response

def bad_request(message):
	response = jsonify({'error':'bad_request', 'message':message})
	response.status_code = 400
	return response

def unauthorized(message):
	response = jsonify({'error':'unauthorized', 'message':message})
	response.status_code = 401
	return response

@api_blueprint.errorhandler(ValidationError)
def validation_error(e):
	return bad_request(e.args[0])