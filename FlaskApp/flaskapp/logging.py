from flaskapp import db
from flaskapp.models import Logs

def log_create(table, user):
	log = Logs(action='Create', table=table, user=user)
	db.session.add(log)
	db.session.commit()

def log_update(table, user):
	log = Logs(action='Update', table=table, user=user)
	db.session.add(log)
	db.session.commit()

def log_delete(table, user):
	log = Logs(action='Delete', table=table, user=user)
	db.session.add(log)
	db.session.commit()