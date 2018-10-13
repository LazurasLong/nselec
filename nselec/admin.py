from flask import (
    Blueprint, render_template
)

from nselec.auth import login_required
from nselec.db import get_db

bp = Blueprint("admin", __name__)

@bp.route("/")
@login_required
def index():
    db = get_db()
    els = db.all()
    return render_template("admin/index.html", els=els)
