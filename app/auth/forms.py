from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from wtforms import ValidationError

from ..models import User

class LoginForm(Form):
	email = StringField('Email', validators=[Required(), Length(1,64), Email()])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log In')

class RegisterForm(Form):
	email = StringField('Email', validators=[Required(), Length(1,64), Email()])
	username = StringField('User name', validators=[Required(), 
													Length(1,64), 
													Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0 , 'username must only have letters, numbers, dots or undersores')])
	password = PasswordField('Password', validators=[Required(),
													 EqualTo('password2', message='Passwords must match')])
	password2 = PasswordField('Confirm Password', validators=[Required()])
	register = SubmitField('Register')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Your email has been registered')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Your username has been registered')

class ChangePasswordForm(Form):
	old_password = PasswordField('Old Password', validators=[Required()])
	password = PasswordField('New Password', validators=[Required(), 
														EqualTo('password2', message='Passwords must match')])
	password2 = PasswordField('Confirm Password', validators=[Required()])
	submit = SubmitField('Update')


class PasswordResetRequestForm(Form):
	email = StringField('Email', validators=[Required(), 
											Length(1,64), 
											Email()])
	submit = SubmitField('Reset Password')

class PasswordResetForm(Form):
	email = StringField('Email', validators=[Required(), Length(1,64), Email()])
	password = PasswordField('Password', validators=[Required(),
													EqualTo('password2', message='Passwords must match')])
	password2 = PasswordField('Confirm Password', validators=[Required()])
	submit = SubmitField('Reset Password')

	def validate_email(self, field):
		if not User.query.filter_by(email=field.data).first():
			raise ValidationError('Unknown email address.')

class ChangeEmailForm(Form):
	email = StringField('New Email', validators=[Required(), Length(1,64), Email()])
	password = PasswordField('Password', validators=[Required()])
	submit = SubmitField('Change Email')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('The email has been registered')
			