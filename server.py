"""Server for Wanderlust app."""

from flask import (Flask, render_template, request, redirect, session, flash)
from model import connect_to_db, db, User, Itinerary, Location
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
                session["user_id"] = user.user_id

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
            session["user_id"] = user.user_id

            flash("Success! Account created. Welcome to Wanderlust.")

            return redirect("/")


@app.route("/itineraries") 
def list_all_itineraries():
    """Return page displaying all itineraries Wanderlust has to offer"""

    itineraries = Itinerary.get_itineraries()

    return render_template("all_itineraries.html", itineraries=itineraries)


@app.route("/itinerary/<itinerary_id>")
def show_itinerary(itinerary_id):
    """Return page displaying itinerary and list of itinerary items"""

    itinerary = Itinerary.get_itinerary_by_itinerary_id(itinerary_id)
    activities = itinerary.activities
    destinations = itinerary.locations

    return render_template("itinerary.html", itinerary=itinerary, activities=activities, destinations=destinations)


@app.route("/create_itinerary", methods=["GET", "POST"])
def create_itinerary():
    """Display form to create a travel itinerary"""

    if request.method == "GET":
        return render_template("create_itinerary.html")
    else:
        itinerary_name = request.form.get("name")
        overview = request.form.get("overview")
        locale = request.form.get("locale")
        territory = request.form.get("territory")
        country = request.form.get("country")
            
        itinerary = Itinerary.create_itinerary(session["user_id"], itinerary_name, overview)
            
        db.session.add(itinerary)
        db.session.commit()

        location = Location.create_location(locale, territory, country)

        db.session.add(location)
        db.session.commit()

        itinerary.locations.append(location)
        db.session.add(itinerary)
        db.session.commit()

        flash(f"Success! {itinerary_name} created.")

        itinerary_id = itinerary.itinerary_id

        return redirect(f"/itinerary/{itinerary_id}")


@app.route("/<itinerary_id>/add_activity", methods=["POST"])
def add_activity(itinerary_id):
    """ """

    return redirect(f"/itinerary/{itinerary_id}")


@app.route("/users")
def show_users():
    """Return page displaying all user profiles"""

    users = User.get_users()

    return render_template("all_users.html", users=users)

@app.route("/user/<username>")
def show_profile(username):
    """Return page displaying user profile and user-curated itineraries"""

    user = User.get_user_by_username(username)
    itineraries = user.itineraries

    return render_template("user_profile.html", display_user=user, user_itineraries=itineraries)


@app.route("/user/<username>/following")
def list_following(username):
    """Return page displaying all users followed by the logged-in user"""

    user = User.get_user_by_username(username)

    following = user.following

    return render_template("following.html", following=following, user=user)


@app.route("/user/<username>/followers")
def list_followers(username):
    """Return page displaying all followers of the logged-in user"""

    user = User.get_user_by_username(username)

    followers = user.followers

    return render_template("followers.html", followers=followers, user=user)


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