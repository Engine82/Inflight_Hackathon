# Imports
from flask import Flask, redirect, render_template, request, session
from flask_session import Session

from sqlalchemy import create_engine, insert, join, select, text, update
from sqlalchemy.orm import sessionmaker

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
    if not session.get("user_id"):
        return render_template("login.html")
    
    else:
        return redirect("/")