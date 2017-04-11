from flask import request,render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user

from . import auth
from ..models import User
from .forms import (LoginForm ,RegisterForm,ChangePasswordForm, PasswordResetRequestForm, 
					PasswordResetForm, ChangeEmailForm)
from app import db
from ..email import send_email



@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('Invalid username or password')
			
	return render_template('/auth/login.html', form=form)

@login_required
@auth.route('/logout')
def logout():
	logout_user()
	flash('You have logged out.')
	return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET','POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		user = User(email=form.email.data,
					username=form.username.data, 	
					password=form.password.data)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
		send_email(user.email, 'Confirm your account', 'auth/email/confirm', token=token, user=user)
		flash('A confirmation email has been sent to your email.')
		return redirect(url_for('main.index'))
	return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash('You have confirmed your account. Thanks!')
	else:
		flash('The confirmation link is invalid or has expired.')
	return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
	if current_user.is_authenticated :
			current_user.ping()
			if not current_user.confirmed \
				and request.endpoint[:5] != 'auth.' \
				and request.endpoint !='static':
					return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_email(current_user.email, 'Confirm your account', 'auth/email/confirm', token=token, user=current_user)
	flash('A new confirmation email has been sent to your email.')
	return redirect(url_for('main.index'))

@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.old_password.data):
			current_user.password = form.password.data
			db.session.add(current_user)
			db.session.commit()
			flash('You have change your password.')
			return redirect(url_for('main.index'))
		else:
			flash('Your old password is invalid')
	return render_template('auth/change_password.html', form=form)

@auth.route('reset', methods=['GET','POST'])
def password_reset_request():
	if not current_user.is_anonymous:
		return redirect(url_for('main.index'))
	form = PasswordResetRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			token = user.generate_reset_token()
			send_email(form.email.data, 'Reset Your Password', 'auth/email/reset_password', user=user, token=token)
			flash('A reset email has been sent to your email')
			return redirect(url_for('auth.login'))
	return render_template('/auth/reset_password.html', form=form)

@auth.route('reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
	if not current_user.is_anonymous:
		return redirect(url_for('main.index'))
	form = PasswordResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None:
			return redirect(url_for('main.index'))
		if user.reset_password(token, form.password.data):
			flash('Your password has been reset')
			return redirect(url_for('auth.login'))
		else:
			return redirect(url_for('main.index'))
	return render_template('auth/reset_password.html', form=form)

@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
	form = ChangeEmailForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.password.data):
			token = current_user.generate_change_email_token(form.email.data)
			send_email(form.email.data, 'Confirm your email address', 'auth/email/change_email', user=current_user, token=token)
			flash('A confirmation email has been sent to your new email')
			return redirect(url_for('main.index'))
		else:
			flash('Invalid password')
	return render_template('auth/change_email.html', form=form)

@auth.route('/change_email/<token>', methods=['GET', 'POST'])
@login_required
def change_email(token):
	if current_user.change_email(token):
		flash('Your email address has been updated')
	else:
		flash('Invalid request')
	return redirect(url_for('main.index'))






