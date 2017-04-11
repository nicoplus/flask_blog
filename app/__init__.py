from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_admin import Admin

from config import config

bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy(use_native_unicode='utf8')
moment = Moment()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
pagedown = PageDown()
from .admin import MyAdminIndexView
admin_instance = Admin(name = 'Flasky', template_mode='bootstrap3', index_view = MyAdminIndexView())


def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])

	bootstrap.init_app(app)
	mail.init_app(app)
	db.init_app(app)
	moment.init_app(app)
	login_manager.init_app(app)
	pagedown.init_app(app)

	from .admin import views	
	admin_instance.init_app(app)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')

	from .api_1_0 import api_blueprint
	app.register_blueprint(api_blueprint)



	return app