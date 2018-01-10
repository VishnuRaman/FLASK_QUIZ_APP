from Flask_Quiz import db

from models import *

db.create_all()
# name, username, password, score
db.session.add(User('admin', 'admin', 'admin', 0))
db.session.commit()