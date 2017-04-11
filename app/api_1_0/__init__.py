from flask import Blueprint


api_blueprint = Blueprint('api', __name__)






from . import authentication, posts, users, comments, errors, resources