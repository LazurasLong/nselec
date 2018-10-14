import functools

from werkzeug.security import check_password_hash, generate_password_hash
from flask import (
    Blueprint, request, session, redirect, url_for, render_template, flash,
    current_app
)

from itsdangerous import TimestampSigner, SignatureExpired, BadSignature

from tinydb import Query

from nselec.db import get_db

def login_required(view):
    # decorator for views/pages for which the user needs to be logged in
    # view is the view function we're decorating
    @functools.wraps(view)
    def wrapped(**kwargs):
        if "user" not in session:
            flash("You need to be logged in to do that.", "error")
            return redirect(url_for('auth.login'))
        else:
            return view(**kwargs)
    return wrapped

bp = Blueprint("auth", __name__)

@bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        error = None
        token = request.form['token']
        ts = TimestampSigner(current_app.secret_key)
        try:
            username = ts.unsign(token, 60*5).decode("utf-8") # 2 minutes
        except SignatureExpired:
            error = "Token has expired"
        except BadSignature:
            error = "Invalid token"
        else:
            db = get_db()
            users = db.table("users")
            users.insert({"username":username,"password":generate_password_hash(request.form['password'])})
        if error is None:
            session.clear()
            flash("Successfully created user!", "success")
            return redirect(url_for("auth.login"))
        else:
            flash(error, "error")
    return render_template("auth/signup.html")

@bp.route("/d/<s>")
def d(s):
    return TimestampSigner(current_app.secret_key).sign(s)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        usertab = db.table("users")
        User = Query()
        entry = usertab.get(User.username == username)
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
