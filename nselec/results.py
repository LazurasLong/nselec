from flask import (
    Blueprint, abort, redirect, url_for, render_template
)

from nselec.db import get_db
from nselec.utils import time_type

bp = Blueprint('results', __name__)

@bp.route('/<int:el_id>')
def results(el_id):
    db = get_db()
    el = db.get(doc_id=el_id)
    if el is None:
        abort(404)
    tt = time_type(el['times']['start'], el['times']['end'])
    if tt == "present":
        return redirect(url_for("vote.election", el_id=el_id))
    elif tt != "past":
        abort(404)
    if el['type'] == "yesno":
        results = process_votes_yesno(el['votes'])
        
