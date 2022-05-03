"""Server for Wanderlust app."""

from flask import (Flask, render_template, request, redirect, session, flash)
from model import connect_to_db, db
import crud
import os

from jinja2 import StrictUndefined

# Create a Flask instance
app = Flask(__name__)

# Tell Jinja to flag as error any undefined variables
app.jinja_env.undefined = StrictUndefined

# Set a secret key to enable use of Flask sessions
app.secret_key = os.environ['FLASK_SECRET_KEY']


@app.route("/")
def show_index():
    """Return homepage"""

    return render_template("homepage.html")


@app.route("/itineraries")
def list_itineraries():
    """Return page displaying all itineraries Wanderlust has to offer"""

    # Ability to filter out by locale, territory, country

    return render_template("all_itineraries.html")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form"""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site"""

    return redirect("/")


@app.route("/user/<username>")
def show_user(username):
    """Return page displaying user profile and list of user curated itineraries"""

    # Need CRUD function to get user object based on username

    return render_template("user_profile.html")


@app.route("/create_itinerary")
def show_create_itinerary():
    """Display form to create a travel itinerary"""

    return render_template("create_itinerary.html")


@app.route("/add_item")
def show_add_item():
    """Display form to add items to a travel itinerary"""

    return render_template("add_item.html")


@app.route("/following")
def list_following():
    """Return page displaying all users followed by the logged-in user"""

    return render_template("user_following.html")


@app.route("/followers")
def list_following():
    """Return page displaying all followers of the logged-in user"""

    return render_template("user_followers.html")


@app.route("/logout")
def process_logout():
    """Delete session and log-out user"""

    return redirect("/")


if __name__ == "__main__":

    # Connect Flask app to the database
    connect_to_db(app)

    # Connect Flask app to the server
    app.run(host="0.0.0.0", debug=True)