from tinydb import TinyDB
from flask import g, current_app

def get_db():
    if 'db' not in g:
        g.db = TinyDB(current_app.config['DATABASE'])
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db) # close the db at the end of the request
