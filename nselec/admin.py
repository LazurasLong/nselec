from datetime import datetime

from flask import (
    Blueprint, render_template, request, flash, redirect, url_for
)

from nselec.auth import login_required
from nselec.db import get_db
from nselec.utils import time_type
from nselec.classes import FancyTime

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

@bp.route("/elections/new/yesno", methods=["GET", "POST"])
@login_required
def new_yesno():
    if request.method == "POST":
        print(request.form)
        name = request.form['name']
        desc = request.form['desc']
        start = request.form['start_date']+" "+request.form['start_time']
        end = request.form['end_date']+" "+request.form['end_time']
        fstr = "%Y-%m-%d %H:%M"
        start_dt = datetime.strptime(start, fstr)
        end_dt = datetime.strptime(end, fstr)
        start_f = FancyTime(start_dt)
        end_f = FancyTime(end_dt)
        db = get_db()
        payload = {
            "name": name,
            "desc": desc,
            "times": {
                "start": start_f,
                "end": end_f
            },
            "type": "yesno",
            "voters": [],
            "votes": []
        }
        db.insert(payload)
        flash("Successfully added new election!", "success")
        return redirect(url_for("admin.elections"))
    return render_template("admin/new_yesno.html")

@bp.route("/elections/new/ranked", methods=["GET", "POST"])
@login_required
def new_ranked():
    if request.method == "POST":
        name = request.form['name']
        desc = request.form['desc']
        start = request.form['start_date']+" "+request.form['start_time']
        end = request.form['end_date']+" "+request.form['end_time']
        fstr = "%Y-%m-%d %H:%M"
        start_dt = datetime.strptime(start, fstr)
        end_dt = datetime.strptime(end, fstr)
        start_f = FancyTime(start_dt)
        end_f = FancyTime(end_dt)
        db = get_db()
        options = request.form.getlist('opt')
        if len(options) < 2:
            flash("You need at least 2 options", "error")
        else:
            payload = {
                "name":name,
                "desc":desc,
                "times": {
                    "start":start_f,
                    "end":end_f
                },
                "voters": [],
                "votes": [],
                "options": options,
                "type": "ranked"
            }
            db.insert(payload)
            flash("Successfully added election!", "success")
            return redirect(url_for('admin.elections'))

    return render_template("admin/new_ranked.html")
