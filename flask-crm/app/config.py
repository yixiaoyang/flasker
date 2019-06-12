#-*- coding:utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SQLALCHEMY_COMMIT_ON_TRARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAIL_SUBJECT_PREFIX = '[FLASK]'
	MAIL_SENDER = 'leon_e@163.com'
	FLASK_ADMIN = os.environ.get('FLASK_ADMIN')
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'Q!W@E#R$'

	# celery
	CELERY_BROKER_URL = 'http://localhost:5672/0'
	CELERY_RESULT_BACKEND = 'http://localhost:5672/0'

	@staticmethod
	def init_app(app):
		pass

class DevConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestConfig(Config):
	TEST = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class ProConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

configs = {
    'development': DevConfig,
    'test': TestConfig,
    'production': ProConfig,
    'default': DevConfig
}
