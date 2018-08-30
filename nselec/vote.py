from flask import (
    Blueprint, render_template, abort
)
from nselec.db import get_db
from nselec.utils import time_type

bp = Blueprint('vote', __name__)

@bp.route("/<int:el_id>")
def election_page(el_id):
    db = get_db()
    el = db.get(doc_id=el_id)
    if el is None:
        abort(404)
        return
    return render_template("vote/yesno.html", el=el)
