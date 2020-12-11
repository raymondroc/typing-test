import os
import time
import random
import string

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Basic configuration, login() adapted from pset8 Finance

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///typingtest.db")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", incorrect=1)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Ensure password confirmation matches
        if request.form.get("password") != request.form.get("confirm-password"):
            return render_template("register.html", nomatch=1)

        # Ensure username is not already taken
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        if len(rows):
            return render_template("register.html", usernametaken=1)

        # Insert user into database
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=request.form.get(
            "username"), hash=generate_password_hash(request.form.get("password")))

        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/test75", methods=["GET", "POST"])
def test75():
    if request.method == "POST":
        score = request.form['time']
        if session["user_id"]:
            db.execute("INSERT INTO scores (time, date, mode, user_id) VALUES (?, ?, ?, ?)",
                       score, time.strftime('%Y-%m-%d %H:%M:%S'), 75, session["user_id"])
        return ''

    else:
        text = []
        for i in range(75):
            text.append(random.choice(string.ascii_lowercase))
        return render_template("test75.html", text=text)


@app.route("/test150", methods=["GET", "POST"])
def test150():
    if request.method == "POST":
        score = request.form['time']
        if session["user_id"]:
            db.execute("INSERT INTO scores (time, date, mode, user_id) VALUES (?, ?, ?, ?)",
                       score, time.strftime('%Y-%m-%d %H:%M:%S'), 150, session["user_id"])
        return ''

    else:
        text = []
        for i in range(150):
            text.append(random.choice(string.ascii_lowercase))
        return render_template("test150.html", text=text)


@app.route("/leaderboard", methods=["GET", "POST"])
def leaderboard():
    r_short = db.execute(
        "SELECT username, MIN(time) FROM scores jOIN users ON scores.user_id = users.id WHERE mode=:mode GROUP BY user_id ORDER BY time ASC LIMIT 20", mode=75)
    records_short = []
    print(r_short)
    counter = 0
    for row in r_short:
        counter += 1
        records_short.append({'rank': counter, 'username': row['username'], 'time': "{:.3f}".format(row['MIN(time)'])})
    for i in range(20 - len(records_short)):
        counter += 1
        records_short.append({'rank': counter, 'username': '', time: ''})

    r_long = db.execute(
        "SELECT username, MIN(time) FROM scores jOIN users ON scores.user_id = users.id WHERE mode=:mode GROUP BY user_id ORDER BY time ASC LIMIT 20", mode=150)
    records_long = []
    counter = 0
    for row in r_long:
        counter += 1
        records_long.append({'rank': counter, 'username': row['username'], 'time': "{:.3f}".format(row['MIN(time)'])})
    for i in range(20 - len(records_long)):
        counter += 1
        records_long.append({'rank': counter, 'username': '', time: ''})

    return render_template("leaderboard.html", records_short=records_short, records_long=records_long)


@app.route("/profile")
@login_required
def profile():
    """View user profile"""
    username = db.execute("SELECT username FROM users WHERE id=:id", id=session["user_id"])[0]['username']

    playcount_short = db.execute("SELECT COUNT(*) FROM scores WHERE mode=:mode AND user_id=:id",
                                 mode=75, id=session["user_id"])[0]['COUNT(*)']
    if playcount_short:
        besttime_short = "{:.3f}".format(db.execute("SELECT MIN(time) FROM scores WHERE mode=:mode AND user_id=:id",
                                    mode=75, id=session["user_id"])[0]['MIN(time)'])
        average_short = "{:.3f}".format(db.execute(
            "SELECT AVG(time) FROM scores WHERE mode=:mode AND user_id=:id ORDER BY date DESC LIMIT 10", mode=75, id=session["user_id"])[0]['AVG(time)'])
    else:
        besttime_short = ''
        average_short = ''

    playcount_long = db.execute("SELECT COUNT(*) FROM scores WHERE mode=:mode AND user_id=:id",
                                mode=150, id=session["user_id"])[0]['COUNT(*)']
    if playcount_long:
        besttime_long = "{:.3f}".format(db.execute("SELECT MIN(time) FROM scores WHERE mode=:mode AND user_id=:id",
                                   mode=150, id=session["user_id"])[0]['MIN(time)'])
        average_long = "{:.3f}".format(db.execute(
            "SELECT AVG(time) FROM scores WHERE mode=:mode AND user_id=:id ORDER BY date DESC LIMIT 10", mode=150, id=session["user_id"])[0]['AVG(time)'])
    else:
        besttime_long = ''
        average_long = ''

    return render_template("profile.html", username=username, playcount_short=playcount_short, besttime_short=besttime_short, average_short=average_short, playcount_long=playcount_long, besttime_long=besttime_long, average_long=average_long)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to homepage
    return redirect("/")