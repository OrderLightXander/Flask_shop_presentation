from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from flaskapp.models import User


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is taken. Please choose a differnt one')

	def validate_email(self, email):
		email = User.query.filter_by(email=email.data).first()
		if email:
			raise ValidationError('That email is taken. Please choose a differnt one')


class LogingForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Log in')


class UpdateAccountForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('That username is taken. Please choose a differnt one')

	def validate_email(self, email):
		if email.data != current_user.email:
			email = User.query.filter_by(email=email.data).first()
			if email:
				raise ValidationError('That email is taken. Please choose a differnt one')


class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	content = TextAreaField('Content', validators=[DataRequired()])
	hot = BooleanField('Hot Post')
	price = StringField('Price')
	release_date = DateField('Release Date')
	volume = StringField('Volume of Book')
	submit = SubmitField('Post')
	language = StringField('Language')
	book_author = StringField('Author')
	book_picture = FileField('Upload Book Picture', validators=[FileAllowed(['jpg', 'png'])])
	fb2 = FileField('Upload FB2 File', validators=[FileAllowed(['fb2'])])


class MorseForm(FlaskForm):
	crypted = StringField('Crypted')
	decrypted = StringField('Decrypted')
	submit = SubmitField('Update Morse Table')


class CommentForm(FlaskForm):
	content = StringField('Comment')
	submit = SubmitField('Post comment')