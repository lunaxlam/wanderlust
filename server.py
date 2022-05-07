"""Server for Wanderlust app."""

from flask import (Flask, render_template, request, redirect, session, flash)
from model import connect_to_db, db, User, Follower, Itinerary, Activity
import os

from jinja2 import StrictUndefined

# Create a Flask instance
app = Flask(__name__)

# Tell Jinja to flag as error any undefined variables
app.jinja_env.undefined = StrictUndefined

# Set a secret key to enable use of Flask sessions
app.secret_key = os.environ['FLASK_SECRET_KEY']


@app.route("/")
def show_welcome():
    """Return homepage"""

    # if user is not logged in:
    return render_template("welcome.html")

    # if user is logged in:
    # return render_template("home.html")

@app.route("/home")
def for_testing_show_home():
    """Return homepage"""

    return render_template("home.html")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form"""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site"""

    # if successfully log in:
    return redirect("/home")

    # if not successfully log in:
    # flash incorrect username or password message
    # return render template login.html


@app.route("/create_user", methods=["GET"])
def create_user():
    """Show create user form"""

    # if successfully log in:
    return render_template("create_user.html")


@app.route("/itineraries") # eventually remove this route
def list_all_itineraries():
    """Return page displaying all itineraries Wanderlust has to offer"""

    # Ability to filter out by locale, territory, country

    return render_template("all_itineraries.html")


@app.route("/itinerary/<itinerary_id>")
def show_itinerary(itinerary_id):
    """Return page displaying itinerary and list of itinerary items"""

    itinerary = Itinerary.get_itinerary_by_itinerary_id(itinerary_id)
    activities = Activity.get_activity_by_itinerary_id(itinerary_id)

    return render_template("itinerary.html", itinerary=itinerary, activities=activities)


@app.route("/create_itinerary")
def show_create_itinerary():
    """Display form to create a travel itinerary"""

    return render_template("create_itinerary.html")


@app.route("/add_item")
def show_add_item():
    """Display form to add items to a travel itinerary"""

    return render_template("add_item.html")

@app.route("/users")
def show_users():
    """Return page displaying all user profiles"""

    users = User.get_users()

    return render_template("all_users.html", users=users)

@app.route("/<username>")
def show_profile(username):
    """Return page displaying user profile and list of user-curated itineraries"""

    user = User.get_user_by_username(username)
    itineraries = Itinerary.get_itinerary_by_user_id(user.user_id)

    return render_template("user_profile.html", display_user=user, user_itineraries=itineraries)


@app.route("/following")
def list_following():
    """Return page displaying all users followed by the logged-in user"""

    return render_template("user_following.html")


@app.route("/followers")
def list_followers():
    """Return page displaying all followers of the logged-in user"""

    return render_template("user_followers.html")


@app.route("/logout")
def process_logout():
    """Delete session and log-out user"""

    return redirect("/")


if __name__ == "__main__":

    # Connect Flask app to the database
    connect_to_db(app)

    # Connect app to the server
    app.run(host="0.0.0.0", debug=True)