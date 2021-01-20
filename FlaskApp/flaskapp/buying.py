from flaskapp import db
from flaskapp.models import User, Post
from flaskapp.logging import log_delete, log_update, log_create
from flask_login import current_user


def buy(User, Post):
    if float(Post.price) <= float(User.wallet):
        Post.owned_users = str(User.id) + ' ' + str(Post.owned_users)
        User.wallet = float(User.wallet) - float(Post.price)
        db.session.add(Post)
        db.session.commit()
        log_update(table=Post.__table__.name, user=current_user.username)


def line_to_arr(Post, user):
    if Post.owned_users:
        owned_users =  Post.owned_users.split()
        for s in owned_users:
            if int(s) == int(user):
                return False
        return True
    else: 
        owned_user = ' '
        return True
