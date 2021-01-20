import os
import secrets
from PIL import Image
from flask import render_template,url_for, flash, redirect, request, abort, send_from_directory
from flaskapp import app, db, bcrypt
from flaskapp.forms import RegistrationForm, LogingForm, UpdateAccountForm, PostForm, MorseForm, CommentForm
from flaskapp.models import User, Post, Morse, Logs, Comments
from flaskapp.crypt import encrypt, decrypt
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp.logging import log_delete, log_update, log_create
from flaskapp.buying import buy, line_to_arr


@app.route('/')
@app.route('/home')
def home():
	users = User.query.all()
	posts = Post.query.all()
	return render_template('home.html', posts=posts,users=users)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    # Appending app path to upload folder path within app root folder
    uploads = os.path.join(app.root_path, 'static/fb2_files', filename)
    # Returning file from appended path
    return send_from_directory(directory=uploads, filename=filename)


@app.route('/morse')
def morse():
	return render_template('morse.html', title='Morse')

@app.route('/mor', methods=['POST'])
def mor(res=sum):
	if request.method == 'POST':
		value = request.form['value']
		operation = request.form['operation']
		if operation == 'decrypt' and value:
			sum = decrypt(value)
			return render_template('morse.html', res=sum)
		elif operation == 'encrypt' and value:
			sum = encrypt(value)
			return render_template('morse.html', res=sum)
		else:
			return render_template('morse.html')

@app.route('/calculator')
def calculator():
	return render_template('calculator.html', title='calculator')

@app.route('/calc', methods=['POST'])
def calc(sum=sum):
	try:
		if request.method == 'POST':
			num1 = request.form['num1']
			num2 = request.form['num2']
			operation = request.form['operation']
			if operation == 'add' and num1 and num2:
				sum = float(num1) + float(num2)
				return render_template('calculator.html', sum=sum)
			elif operation == 'substract' and num1 and num2:
				sum = float(num1) - float(num2)
				return render_template('calculator.html', sum=sum)
			elif operation == 'multiply' and num1 and num2:
				sum = float(num1) * float(num2)
				return render_template('calculator.html', sum=sum)
			elif operation == 'divide' and num1 and num2:
				sum = float(num1) / float(num2)
				return render_template('calculator.html', sum=sum)
		else:
			return render_template('calculator.html')
	except ZeroDivisionError as e:
		return render_template('calculator.html', sum="You can't divide by zero")
	



def move_forward():
	return render_template('morse.html', title='Morse', form=form, morse=morse)

@app.route('/store')
def store():
	users = User.query.all()
	posts = Post.query.all()
	return render_template('store.html', posts=posts, users=users, title='Store')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		log_create(table=User.__table__.name, user=form.username.data)
		flash('Your account has been created! You are now able to log in', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LogingForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login unseccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Log In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
	output_size = (500, 500)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn

def save_fb2(form_file):
	file_path = os.path.join(app.root_path, 'static/fb2_files', form_file.filename)
	form_file.save(file_path)
	return form_file.filename

def save_book_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/book_pics', picture_fn)
	output_size = (500, 500)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required 
def account():
	users = User.query.all()
	posts = Post.query.all()
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		log_update(table=User.__table__.name, user=current_user.username)
		flash('Your account has been updated!', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file=image_file, form=form, posts=posts, users=users)

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		if form.book_picture.data:
			picture_file = save_book_picture(form.book_picture.data)
		else: picture_file = None
		"""if form.fb2.data:
			fb2 = save_fb2(form.fb2.data)
		else: fb2 = None"""
		post = Post(title=form.title.data, content=form.content.data, author=current_user, language=form.language.data, 
			top=form.hot.data, price=form.price.data, volume=form.volume.data, 
			release_date=form.release_date.data, book_author=form.book_author.data, image_file=picture_file, fb2_file=None)
		db.session.add(post)
		db.session.commit()
		log_create(table=Post.__table__.name, user=current_user.username)
		flash('Your post has been created!', 'success')
		return redirect(url_for('home'))
	return render_template('create_post.html', title='New Post',
		form=form, legend='New Post')


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
	post = Post.query.get_or_404(post_id)
	comments = Comments.query.filter_by(post=post_id).all()
	form = CommentForm()
	if form.validate_on_submit():
		comment = Comments(content=form.content.data, author=current_user.username, author_id=current_user.id, post=post_id)
		db.session.add(comment)
		db.session.commit()
		log_create(table=Comments.__table__.name, user=current_user.username)
		flash('Your comment has been posted!', 'success')
		return redirect('/post/{}'.format(post_id))
	return render_template('post.html', title=post.title, post=post, form=form, comments=comments)

@app.route('/post/<int:post_id>/buy', methods=['GET','POST'])
@login_required
def buy_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(current_user.id)
    if line_to_arr(post, user.id):
        buy(user,post)
        flash('Operation was sucessfull')
    return redirect(url_for('home'))

@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	form = PostForm()
	if post.author != current_user and not current_user.admin:
		abort(403)
	if form.validate_on_submit():
		if form.book_picture.data:
			picture_file = save_book_picture(form.book_picture.data)
			post.image_file = picture_file
		if form.fb2.data:
			post.fb2_file = save_fb2(form.fb2.data)
		post.title = form.title.data
		post.content = form.content.data
		post.top = form.hot.data
		post.price = form.price.data
		post.release_date = form.release_date.data
		post.volume = form.volume.data
		post.language = form.language.data
		post.book_author = form.book_author.data
		db.session.commit()
		log_update(table=Post.__table__.name, user=current_user.username)
		flash('Your post has been updated!', 'success')
		return redirect(url_for('post', post_id=post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
		form.hot.data = post.top
		form.price.data = post.price
		form.release_date.data = post.release_date
		form.volume.data = post.volume
		form.language.data = post.language
		form.book_author.data = post.book_author
	image_file = url_for('static', filename='profile_pics/' + post.image_file)
	return render_template('create_post.html', title='Update Post', 
		form=form, legend='Update Post', image_file=image_file)


"""@app.route('/post/<int:post_id>/delete_post', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user and not current_user.admin:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    log_delete(table=Post.__table__.name, user=current_user.username)
    flash('Your post has been deleted!', 'success')
    next_page = request.referrer
    #return redirect(next_page) if next_page else redirect(url_for('home'))
    return redirect(url_for('home'))"""


@app.route('/sql_admin', methods=['GET', 'POST'])
@login_required 
def sql_admin():
	posts = Post.query.all()
	users = User.query.all()
	morse = Morse.query.all()
	logs = Logs.query.all()
	comments = Comments.query.all()
	form = MorseForm()
	if not current_user.admin:
		abort(403)
	if form.validate_on_submit():
		morse = Morse(crypted=form.crypted.data, decrypted=form.decrypted.data)
		db.session.add(morse)
		db.session.commit()
		log_create(table=Morse.__table__.name, user=current_user.username)
		flash('Your morse table has been updated!', 'success')
		return redirect(url_for('sql_admin'))
	return render_template('sql_admin.html', title='Database', users=users, posts=posts, morse=morse, logs=logs, comments=comments, form=form)

@app.route('/user/<int:user_id>/update', methods=['POST'])
@login_required
def update_user(user_id):
	user = User.query.get_or_404(user_id)
	if not current_user.admin:
		abort(403)
	if user.admin:
		user.admin = False
	else:
		user.admin = True
	db.session.commit()
	log_update(table=User.__table__.name, user=current_user.username)
	flash('User has been updated!', 'success')
	return redirect(url_for('sql_admin'))


@app.route('/user/<int:user_id>')
def user(user_id):
	user = User.query.get_or_404(user_id)
	return render_template('user.html', title=user.username, user=user)

@app.route('/user/<int:user_id>/remove_account', methods=['POST'])
@login_required
def remove_account(user_id):
	user = User.query.get_or_404(user_id)
	if not current_user.admin:
		abort(403)
	db.session.delete(user)
	db.session.commit()
	log_delete(table=User.__table__.name, user=current_user.username)
	flash('This user and all his posts has been removed!', 'success')
	return redirect(url_for('sql_admin'))


@app.route('/delete_morse/<int:id>')
def delete_morse(id):
    item_to_delete = Morse.query.get_or_404(id)
    db.session.delete(item_to_delete)
    db.session.commit()
    log_delete(table=Morse.__table__.name, user=current_user.username)
    next_page = request.referrer
    return redirect(next_page) if next_page else redirect(url_for('home'))

@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    item_to_delete = Post.query.get_or_404(post_id)
    db.session.delete(item_to_delete)
    db.session.commit()
    log_delete(table=Post.__table__.name, user=current_user.username)
    next_page = request.args.get('next')
    return redirect(next_page) if next_page else redirect(url_for('home'))

@app.route('/delete_comment/<int:id>')
def delete_comment(id):
	item_to_delete = Comments.query.get_or_404(id)
	db.session.delete(item_to_delete)
	db.session.commit()
	log_delete(table=Comments.__table__.name, user=current_user.username)
	next_page = request.referrer 
	return redirect(next_page) if next_page else redirect(url_for('home'))
