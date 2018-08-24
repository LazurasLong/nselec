# blueprint containing the main election list
from flask import (
    Blueprint, render_template
)
from nselec.db import get_db
from nselec.utils import time_type
from nselec.classes import FancyTime
import datetime as dt
bp = Blueprint('election_list', __name__)

@bp.route('/')
def election_list():
    db = get_db()
    elections = db.all()
    # we need to sort these into "past", "present" and "future"
    categories = {'past':[],'present':[],'future':[]}
    for el in elections:
        tt = time_type(el['times']['start'], el['times']['end'])
        categories[tt].append(el)

    return render_template("election_list/election_list.html", **categories)
