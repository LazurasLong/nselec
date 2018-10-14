from flask import (
    Blueprint, render_template
)

from nselec.auth import login_required
from nselec.db import get_db
from nselec.utils import time_type

bp = Blueprint("admin", __name__)

@bp.route("/")
@login_required
def index():
    return render_template("admin/index.html")

@bp.route("/users")
@login_required
def users():
    pass

@bp.route("/elections")
@login_required
def elections():
    db = get_db()
    els = db.all()
    categories = {"past":[],"present":[],"future":[]}
    for el in els:
        tt = time_type(el['times']['start'], el['times']['end'])
        categories[tt].append(el)

    return render_template("admin/elections.html", **categories)

@bp.route("/elections/new/yesno")
@login_required
def new_yesno():
    return render_template("admin/new_yesno.html")
