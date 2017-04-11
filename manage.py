# coding=utf-8

import os

from app import  db, create_app

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

COV = None
if os.environ.get('FLASKY_COVERAGE'):
	import coverage
	COV = coverage.coverage(branch=True, include='app/*')
	COV.start()

app = create_app(os.environ.get('FLASKY_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app,db)

manager.add_command('db', MigrateCommand)

@manager.command
def test(coverage=False):
	'''Run the unit tests'''
	if coverage and not os.environ.get('FLASKY_COVERAGE'):
		import sys
		print 'executable:%s____argv:%s'%(sys.executable, sys.argv)
		os.environ['FLASKY_COVERAGE'] = '1'
		os.execvp(sys.executable, [sys.executable]+sys.argv)		
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)
	if COV:
		COV.stop()
		COV.save()
		print('Coverage Summary')
		COV.report()
		basedir = os.path.abspath(os.path.dirname(__file__))
		covdir = os.path.join(basedir, 'tmp/coverage')
		COV.html_report(directory=covdir)
		print 'HTML  version: file://%s/index.html' %covdir
		COV.erase()

if __name__ == '__main__':
	manager.run()