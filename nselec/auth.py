import functools

from werkzeug.security import check_password_hash
from flask import (
    Blueprint, request, session, redirect, url_for, render_template, flash
)
from tinydb import Query

from nselec.db import get_db

def login_required(view):
    # decorator for views/pages for which the user needs to be logged in
    # view is the view function we're decorating
    @functools.wraps(view)
    def wrapped(**kwargs):
        print(session)
        if "user" not in session:
            flash("You need to be logged in to do that.", "error")
            return redirect(url_for('auth.login'))
        else:
            return view(**kwargs)
    return wrapped

bp = Blueprint("auth", __name__)

@bp.route("/d")
def dbg():
    return str(session)

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(username, password)
        db = get_db()
        error = None
        usertab = db.table("users")
        User = Query()
        entry = usertab.get(User.username == username)
        print(entry)
        if entry == None or not check_password_hash(entry.get('password', None), password):
            flash("Invalid username or password!")
        else:
            # valid login, hooray!
            session.clear()
            session['user'] = username
            flash("Login successful!", "success")
            return redirect(url_for('index'))
    return render_template("auth/login.html")

@bp.route("/logout")
def logout():
    session.clear()
    flash("Successfully logged out!", "success")
    return redirect(url_for("index"))
