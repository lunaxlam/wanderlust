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

    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def process_login():
    """Log user into site"""

    if request.method == "GET":
        return render_template("login.html")
    else:
        # Authenticate the user
        email = request.form.get("email")

        user = User.get_user_by_email(email)

        if user:
            password = request.form.get("password")
            
            if password == user.password:
                # Add user to the session via user's username
                session["user"] = f"{user.username}"

                flash(f"Success! Welcome back to Wanderlust, {user.username}")
                
                return redirect("/")
            else:
                flash("Incorrect password.")
                
                return redirect("/login")
        else:
            flash("Username does not exist!")
            
            return redirect("/create_user")


@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    """Register a new user."""

    if request.method == "GET":
        return render_template("create_user.html")
    else:
        # Check to see if user already exists in database
        email = request.form.get("email")

        if (User.get_user_by_email(email)):
            flash("Your account already exists! Please log-in instead.")

            return redirect("/login")
        else: 
            password = request.form.get("password")
            username = request.form.get("username")
            fname = request.form.get("fname")
            lname = request.form.get("lname")
            locale = request.form.get("locale")
            territory = request.form.get("territory")
            country = request.form.get("country")
            about_me = request.form.get("about_me")

            user = User.create_user(email, 
                                        password,
                                        username,
                                        fname,
                                        lname,
                                        locale,
                                        territory,
                                        country,
                                        about_me)
            
            db.session.add(user)
            db.session.commit()

            # Add user to the session via user's primary key
            session["user"] = f"{user.username}"

            flash("Success! Account created. Welcome to Wanderlust.")

            return redirect("/")



@app.route("/itineraries") # eventually remove this route
def list_all_itineraries():
    """Return page displaying all itineraries Wanderlust has to offer"""

    itineraries = Itinerary.get_itineraries()

    return render_template("all_itineraries.html", itineraries=itineraries)


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


@app.route("/<username>/following")
def list_following(username):
    """Return page displaying all users followed by the logged-in user"""

    user = User.get_user_by_username(username)

    user_id = user.user_id

    following = Follower.get_following_by_follower_id(user_id)

    return render_template("following.html", following=following)


@app.route("/<username>/followers")
def list_followers(username):
    """Return page displaying all followers of the logged-in user"""

    user = User.get_user_by_username(username)

    user_id = user.user_id

    followers = Follower.get_followers_by_user_followed_id(user_id)

    return render_template("followers.html", followers=followers)


@app.route("/logout")
def process_logout():
    """Delete session and log-out user"""

    session.pop("user")

    flash("Logged out.")

    return redirect("/")


if __name__ == "__main__":

    # Connect Flask app to the database
    connect_to_db(app)

    # Connect app to the server
    app.run(host="0.0.0.0", debug=True)