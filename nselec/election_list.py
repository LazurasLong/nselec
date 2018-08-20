# blueprint containing the main election list
from flask import (
    Blueprint, render_template
)
from nselec.db import get_db

bp = Blueprint('election_list', __name__)

@bp.route('/')
def election_list():
    return render_template("election_list/election_list.html")
