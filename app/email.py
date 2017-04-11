from . import mail

from flask_mail import Message
from flask import current_app, render_template

from threading import Thread

def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)

def send_email(to, subject, template, **kw):
	app = current_app._get_current_object()
	msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+' '+ subject, sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
	msg.body = render_template(template+ '.txt', **kw)
	msg.html = render_template(template+ '.html', **kw)
	th = Thread(target=send_async_email, args=[app, msg])
	th.start()
	return th