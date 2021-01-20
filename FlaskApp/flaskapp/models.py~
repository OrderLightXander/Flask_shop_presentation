from datetime import datetime
from flaskapp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    roles = db.Column(db.Integer, nullable=False, default='0')
    wallet = db.Column(db.Float, nullable=False, default='0')

    def __repr__(self):
        return f'User("{self.username}", "{self.email}", "{self.image_file}", "{self.admin}")'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    data_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    release_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    volume = db.Column(db.String(20), nullable=False, default='Undefined')
    price = db.Column(db.String(20), nullable=False, default='Out of stock')
    top = db.Column(db.Boolean, nullable=False, default=False)
    language = db.Column(db.String(40), nullable=False, default='Undefined')
    book_author = db.Column(db.String(40), nullable=False, default='Undefined')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    fb2_file = db.Column(db.String(40), nullable=True)
    owned_users = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'Post("{self.title}", "{self.data_posted}", "{self.price}", "{self.image_file}")'

class Morse(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	crypted = db.Column(db.String(10), nullable=False)
	decrypted = db.Column(db.String(10), nullable=False)

	def __repr__(self):
		return f'Morse("{self.crypted}", "{self.decrypted}")'


class Logs(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	action = db.Column(db.String(50), nullable=False)
	table = db.Column(db.String(50), nullable=False)
	user = db.Column(db.String(50), nullable=False)

	def __repr__(self):
		return f'Logs("{self.action}", "{self.table}", "{self.date_time}", "{self.user}")'

class Comments(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.String(3000), nullable=False)
	author = db.Column(db.Integer)
	author_id = db.Column(db.Integer)
	post = db.Column(db.Integer)
