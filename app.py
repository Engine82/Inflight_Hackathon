# Imports
from flask import Flask, redirect, render_template, request, session
from flask_session import Session

from sqlalchemy import create_engine, insert, join, select, text, update
from sqlalchemy.orm import sessionmaker

from db_setup import Base, Users, Days

from datetime import datetime

# Configure app
app = Flask(__name__)

# Configure login session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure db
engine = create_engine("sqlite:///database.db", echo=True)
session_factory = sessionmaker(bind=engine)
db = session_factory()


# HOME
@app.route("/", methods=["GET", "POST"])
def index():

    # If logged in, display homepage; if not logged in, redirect to login page
    if not session.get("user_id"):
        return redirect("/login")

    else:
        return render_template("index.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        
        # get user inputs
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return render_template("error.html", error="Username required")

        if not password:
            return render_template("error.html", error="Password required")

        user_data = db.execute(
            select(Users.username, Users.password, Users.id)
            .where(Users.username == username)
        )
        try: 
            usr_data = user_data.mappings().all()[0]

        except:
            return render_template("error.html", error="User not found in db")

        if username != usr_data['username']:
            return render_template("error.html", error="Username invalid")

        if password != usr_data['password']:
            return render_template("error.html", error="Password invalid")

        session['user_id'] = usr_data['id']

        return redirect("/")

    else:
        
        return render_template("login.html")


# Add day:
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":

        mtn = request.form.get("mtn")
        print(mtn)
        if mtn == str(0):
            return render_template("error.html", error="Select Mountain")
        
        date = request.form.get("date")
        print(date)
        if date == "":
            return render_template("error.html", error="Enter Date")
        new_date = datetime.strptime(date, '%Y-%m-%d')
        print(new_date)

        hours = request.form.get("hours")
        print(hours)
        if hours == "":
            return render_template("error.html", error="Enter Hours")


        stmt = insert(Days).values(
            user = session['user_id'],
            mountain = mtn,
            date = new_date,
            hours = hours
        )
        db.execute(stmt)
        db.commit()


        return redirect("/")

    else:
        return render_template("add.html")


# Stats:
@app.route("/stats", methods=["GET"])
def stats():
    return render_template("stats.html")