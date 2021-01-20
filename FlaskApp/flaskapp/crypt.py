from flaskapp.models import Morse

def encrypt(value):
	alphabet = Morse.query.all()
	encrypted = ''
	dicte = row2dict_encrypt(alphabet)
	for i in value.lower():
		if i == " ":
			encrypted+= " / "
		elif dicte.get(i):
			encrypted+= dicte.get(i) + ' '
	return encrypted


def decrypt(value):
	alphabet = Morse.query.all()
	decrypted = ''
	dicte = row2dict_decrypt(alphabet)
	for i in value.split():
		if i == '/':
			decrypted+= " "
		elif dicte.get(i):
			decrypted+= dicte.get(i)
	return decrypted


def row2dict_encrypt(object):
	encrypted = {}
	for i in object:
		encrypted.update({i.decrypted:i.crypted})
	return encrypted

def row2dict_decrypt(object):
	encrypted = {}
	for i in object:
		encrypted.update({i.crypted:i.decrypted})
	return encrypted