from datetime import datetime, timezone
from tinydb import TinyDB
from tinydb_serialization import Serializer, SerializationMiddleware
from flask import g, current_app
from nselec.classes import FancyTime

sz = SerializationMiddleware()

class DatetimeSerializer(Serializer):
    OBJ_CLASS = FancyTime
    def encode(self, obj):
        return str(obj.dt.replace(tzinfo=timezone.utc).timestamp())
    def decode(self, s):
        return FancyTime(datetime.fromtimestamp(float(s), timezone.utc))
sz.register_serializer(DatetimeSerializer(), 'timestamp')

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
