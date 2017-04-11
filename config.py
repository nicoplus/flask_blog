import os

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
	FLASKY_MAIL_SENDER = '290236713@qq.com'
	FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or '1960422464@qq.com'
	FLASKY_POSTS_PER_PAGE = os.environ.get('FLASKY_POSTS_PER_PAGE') or 10
	FLASKY_FOLLOWERS_PER_PAGE = os.environ.get('FLASKY_FOLLOWERS_PER_PAGE') or 10
	FLASKY_FOLLOWED_PER_PAGE = os.environ.get('FLASKY_FOLLOWED_PER_PAGE') or 10
	FLASKY_COMMENTS_PER_PAGE = os.environ.get('FLASKY_COMMENTS_PER_PAGE') or 10

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	MAIL_SERVER = 'smtp.qq.com'
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '290236713@qq.com'
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'vjnlmcjpzisabibf'
	SQLALCHEMY_DATABASE_URI = 'mysql://web:web@localhost/flask'

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'mysql://web:web@localhost/flasktest'
	WTF_CSRF_ENABLED  = False

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'mysql://web:web@localhost/flaskproduct'


config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'produciton': ProductionConfig,
	'default': DevelopmentConfig
}