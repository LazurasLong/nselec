from tinydb import TinyDB
from tinydb_serialization import Serializer, SerializationMiddleware
from flask import g, current_app

from datetime import datetime as dt

class DatetimeSerializer(Serializer):
    OBJ_CLASS = dt
    def encode(self, obj):
        return obj.isoformat()
    def decode(self, s):
        return dt.fromisoformat(s)
sz = SerializationMiddleware()
sz.register_serializer(DatetimeSerializer(), 'Datetime')


def get_db():
    if 'db' not in g:
        g.db = TinyDB(current_app.config['DATABASE'], storage=sz)
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db) # close the db at the end of the request
