"""Server for Wanderlust app."""

from flask import Flask, render_template, request, redirect, session, flash, jsonify
from model import connect_to_db, db, User, Itinerary, Location, Activity, Country
import os
import requests

from jinja2 import StrictUndefined

# Create a Flask instance
app = Flask(__name__)

# Tell Jinja to flag as error any undefined variables
app.jinja_env.undefined = StrictUndefined

# Set a secret key to enable use of Flask sessions
app.secret_key = os.environ['FLASK_SECRET_KEY']

# Google API key
API_KEY = os.environ['GOOGLE_API_KEY']


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

        countries = Country.get_countries()

        return render_template("create_user.html", countries=countries)
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


@app.route("/create_itinerary", methods=["GET", "POST"])
def create_itinerary():
    """Display form to create a travel itinerary"""

    if request.method == "GET":

        countries = Country.get_countries()
        return render_template("create_itinerary.html", countries=countries)
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


@app.route("/itineraries") 
def list_all_itineraries():
    """Return page displaying all itineraries Wanderlust has to offer"""

    itineraries = Itinerary.get_itineraries()
    locations = Location.get_locations()

    return render_template("all_itineraries.html", itineraries=itineraries, locations=locations)


@app.route("/api/itineraries/by_locale")
def itinerary_locale_info():
    """JSON information about itineraries by locale"""

    db_itineraries_locale = {}

    locale = request.args.get("locale")

    itineraries = Itinerary.get_itinerary_by_locale(locale)

    for i, itinerary in enumerate(itineraries):
        db_itineraries_locale[f"{i}"] = {"itinerary_id": itinerary.itinerary_id,
                                        "itinerary_name": itinerary.itinerary_name,
        }

    return jsonify(db_itineraries_locale)


@app.route("/api/itineraries/by_territory")
def itinerary_territory_info():
    """JSON information about itineraries by territory"""

    db_itineraries_territory = {}

    territory = request.args.get("territory")

    itineraries = Itinerary.get_itinerary_by_territory(territory)

    for i, itinerary in enumerate(itineraries):
        db_itineraries_territory[f"{i}"] = {"itinerary_id": itinerary.itinerary_id,
                                        "itinerary_name": itinerary.itinerary_name,
        }

    return jsonify(db_itineraries_territory)


@app.route("/api/itineraries/by_country")
def itinerary_country_info():
    """JSON information about itineraries by country"""

    db_itineraries_country = {}

    country = request.args.get("country")

    itineraries = Itinerary.get_itinerary_by_country(country)

    for i, itinerary in enumerate(itineraries):
        db_itineraries_country[f"{i}"] = {"itinerary_id": itinerary.itinerary_id,
                                        "itinerary_name": itinerary.itinerary_name,
        }

    return jsonify(db_itineraries_country)


@app.route("/itinerary/<itinerary_id>")
def show_itinerary(itinerary_id):
    """Return page displaying itinerary and list of itinerary items"""

    itinerary = Itinerary.get_itinerary_by_itinerary_id(itinerary_id)
    destinations = itinerary.locations
   
    session["itinerary_id"] = itinerary_id

    return render_template("itinerary.html", itinerary=itinerary, destinations=destinations)


@app.route("/itinerary/<itinerary_id>/delete_itinerary")
def delete_itinerary(itinerary_id):
    """Delete itinerary from database"""

    Itinerary.delete_itinerary(itinerary_id)

    return redirect(f"/user/{session['user']}")


@app.route("/itinerary/<itinerary_id>/search")
def search_place(itinerary_id):
    """Search for places on Google Places"""

    keyword = request.args.get("keyword", "")
    locale = request.args.get("locale", "")
    territory = request.args.get("territory", "")
    country = request.args.get("country", "")

    query = f"{keyword}+{locale}+{territory}+{country}"

    endpoint = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    payload = {"query": query, "key": API_KEY}

    response = requests.get(endpoint, params=payload)

    data = response.json()

    results = data["results"]

    if len(results) > 0:
        return render_template("search_results.html", itinerary_id=itinerary_id, results=results, data=data)
    else:
        flash("Search is too ambiguous. Try again.")
        return redirect(f"/itinerary/{itinerary_id}")


@app.route("/itinerary/<itinerary_id>/search/<next_page_token>")
def search_place_next(itinerary_id, next_page_token):
    """Search for additional results on Google Places"""

    return redirect("/")


@app.route("/itinerary/<itinerary_id>/search/<place_id>/details")
def view_place_details(itinerary_id, place_id):
    """View details for a location on Google Places"""
    
    endpoint = "https://maps.googleapis.com/maps/api/place/details/json"
    payload = {"place_id": place_id, "key": API_KEY}

    response = requests.get(endpoint, params=payload)

    data = response.json()

    results = data["result"]

    # # Store in sessions object to use later
    session["place_data"] = {"name": results["name"],
                            "location": results["geometry"]["location"],
                            "address": results["formatted_address"],
                            "place_url": results["url"]}

    return render_template("place_details.html",
                            API_KEY=API_KEY,
                            itinerary_id=itinerary_id,
                            results=results)


@app.route("/api/search_place_data")
def search_place_data():
    """JSON information of a search place"""

    return jsonify(session["place_data"])


@app.route("/itinerary/<itinerary_id>/<place_id>/add_activity", methods=["GET", "POST"])
def add_activity(itinerary_id, place_id):
    """Create an activity and add to itinerary"""

    if request.method == "GET":
        return render_template("add_activity.html", itinerary_id=itinerary_id, place_id=place_id)
    else:
        itinerary_id = itinerary_id
        place_id = place_id
        activity_name = request.form.get("name")
        start = request.form.get("start")
        end = request.form.get("end")
        notes = request.form.get("notes")

        new_activity = Activity.create_activity(itinerary_id, activity_name, start, end, notes, place_id)

        db.session.add(new_activity)
        db.session.commit()

        return redirect(f"/itinerary/{itinerary_id}")


@app.route("/api/saved_activities")
def saved_place_data():
    """JSON information about previously saved activities including place_id data"""

    db_activities = {}

    activities = Activity.get_activities_by_itinerary_id(session["itinerary_id"])

    for i, activity in enumerate(activities):

        endpoint = "https://maps.googleapis.com/maps/api/place/details/json"
        payload = {"place_id": activity.place_id, 
                    "key": API_KEY}

        response = requests.get(endpoint, params=payload)
        data = response.json()
        
        results = data["result"] 

        db_activities[f"{i}"] = {"activity_id": activity.activity_id,
                                "itinerary_id": activity.itinerary_id,
                                "activity_name": activity.activity_name,
                                "dates": activity.dates,
                                "start": activity.start_time,
                                "end": activity.end_time,
                                "notes": activity.notes,
                                "place_id": activity.place_id,
                                "results": results
        }
        
    return jsonify(db_activities)


@app.route("/api/delete_activity")
def delete_activity():
    """Delete activity from database"""

    activity_id = request.args.get("activity_id")

    Activity.delete_activity(activity_id)

    return {"success": True,
            "status": f"Success! Activity deleted."}


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

    flash("Goodbye!")

    return redirect("/")


if __name__ == "__main__":

    # Connect Flask app to the database
    connect_to_db(app)

    # Connect app to the server
    app.run(host="0.0.0.0", debug=True)