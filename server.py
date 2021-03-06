"""Server for Wanderlust app"""


from flask import Flask, render_template, request, redirect, session, flash, jsonify
from flask_bcrypt import Bcrypt
from jinja2 import StrictUndefined
from model import connect_to_db, db, User, Follower, Itinerary, Location, Activity, Country
import os, requests

# import sys

# Create a Flask instance
app = Flask(__name__)

# Tell Jinja to flag as error any undefined variables
app.jinja_env.undefined = StrictUndefined

# Flask API key to enable use of session
app.secret_key = os.environ['FLASK_SECRET_KEY']

# Google API key
API_KEY = os.environ['GOOGLE_API_KEY']
API_KEY_FRONT = os.environ['GOOGLE_API_KEY_FRONTEND']

### Standard Routes  ###

@app.route("/")
def show_welcome():
    """Return homepage"""

    session["user"] = None

    return render_template("home.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site"""

    email = request.form.get("email")
    user = User.get_user_by_email(email)

    if user:
        password_candidate = request.form.get("password")

        if Bcrypt().check_password_hash(user.password, password_candidate):
            session["user"] = f"{user.username}"
            session["user_id"] = user.user_id

            flash(f"Success! Welcome back to Wanderlust, {user.fname}!")
            
            return redirect(f"/user/{session['user']}")
        else:
            flash("Incorrect password.")
            
            return redirect("/")
    else:
        flash("Username does not exist!")
        
        return redirect("/")


@app.route("/logout")
def process_logout():
    """Delete session and log-out user"""

    session.pop("user")

    return redirect("/")


### User Routes  ###

@app.route("/create_account", methods=["POST", "GET"])
def create_user():
    """Register a new user."""


    if request.method == "GET":
        return render_template("create_account.html") 
    else: 

        email = request.form.get("email")

        if (User.get_user_by_email(email)):
            flash("Your account already exists! Please log-in instead.")
            return redirect("/")
        else:

            formData = dict(request.form)

            password = formData["password"]
            username = formData["username"]
            fname = formData["fname"]
            lname = formData["lname"]
            locale = formData["locale"]
            territory = formData["territory"]
            country = formData["country"]
            about_me = formData["about_me"]

            # Hash and add salt to the password
            password_hash = Bcrypt().generate_password_hash(password).decode('utf-8')

            user = User.create_user(email, 
                                    password_hash,
                                    username,
                                    fname,
                                    lname,
                                    locale,
                                    territory,
                                    country,
                                    about_me)

            session["user"] = f"{user.username}"
            session["user_id"] = user.user_id

            flash("Success! Account created. Welcome to Wanderlust!")

            return redirect(f"/user/{session['user']}")


@app.route("/users")
def show_users():
    """Return page displaying all user profiles"""

    users = User.get_users()

    user_photos = []

    for user in users:

        endpoint = "https://randomuser.me/api/"

        response = requests.get(endpoint)
        data = response.json()

        user_photos.append(data["results"][0]["picture"]["large"])

    return render_template("all_users.html", users=users, user_photos=user_photos)


@app.route("/user/<username>")
def show_profile(username):
    """Return page displaying user profile and user-curated itineraries"""

    session["viewed_user"] = username

    user = User.get_user_by_username(username)
    itineraries = user.itineraries
    following = user.following
    followers = user.followers

    return render_template("user_profile.html", user=user, user_itineraries=itineraries, following=following, followers=followers, API_KEY=API_KEY_FRONT)


@app.route("/user/edit_user", methods=["POST", "GET"])
def edit_user():
    """Edit the logged-in user"""

    user = User.get_user_by_user_id(session["user_id"])

    if request.method == "GET":
        return render_template("create_account.html") 
    else:

        formData = dict(request.form)

        email = formData["email"]
        password = formData["password"]
        username = formData["username"]
        fname = formData["fname"]
        lname = formData["lname"]
        locale = formData["locale"]
        territory = formData["territory"]
        country = formData["country"]
        about_me = formData["about_me"]

        if password != "":
            password = Bcrypt().generate_password_hash(password).decode('utf-8')
        
        user.edit_user(email=email, 
                            password=password, 
                            username=username, 
                            fname=fname, 
                            lname=lname, 
                            locale=locale, 
                            territory=territory, 
                            country=country, 
                            about_me=about_me)
        
        flash("Account updated!")

        return redirect(f"/user/{session['user']}")


@app.route("/user/<username>/follow_me")
def follower_user(username):
    """Save user to logged-in user's following page"""

    user_follower = session["user_id"]
    user_followed = User.get_user_by_username(username)
    user_followed_id = user_followed.user_id

    followers = user_followed.followers

    for follower in followers:
        if follower.follower_id == user_follower:
            flash(f"You are already following {username}!")
            return redirect(f"/user/{username}")

    Follower.create_follower(follower_id=user_follower, user_followed_id=user_followed_id)

    flash(f"Success! You are now following {username}")

    return redirect(f"/user/{username}")


### Itinerary Routes  ###

@app.route("/create_itinerary", methods=["POST"])
def create_itinerary():
    """Display form to create a travel itinerary"""

    formData = dict(request.form)

    itinerary_name = formData["name"]
    overview = formData["overview"]
    locale = formData["locale"]
    territory = formData["territory"]
    country = formData["country"]
        
    itinerary = Itinerary.create_itinerary(session["user_id"], itinerary_name, overview)
    location = Location.create_location(locale, territory, country)

    itinerary.locations.append(location)
    db.session.add(itinerary)
    db.session.commit()

    flash(f"Success! {itinerary_name} created.")

    itinerary_id = itinerary.itinerary_id

    return redirect(f"/itinerary/{itinerary_id}")


@app.route("/itineraries") 
def list_all_itineraries():
    """Return page displaying all itineraries Wanderlust has to offer"""

    locales = []
    territories = []
    countries = []

    locations = Location.get_locations()
    itineraries = Itinerary.get_itineraries()

    for location in locations:
        if location.locale not in locales:
            locales.append(location.locale)
        if location.territory not in territories:
            territories.append(location.territory)
        if location.country not in countries:
            countries.append(location.country)
    
    locales.sort()
    territories.sort()
    countries.sort()

    return render_template("all_itineraries.html", locales=locales, territories=territories, countries=countries, itineraries=itineraries)


@app.route("/itinerary/<itinerary_id>", methods =["POST", "GET"])
def show_itinerary(itinerary_id):
    """Return page displaying itinerary and list of itinerary items"""

    session["itinerary_id"] = itinerary_id

    if request.method == "GET":
        itinerary = Itinerary.get_itinerary_by_itinerary_id(itinerary_id)
        destinations = itinerary.locations

        activities = Activity.get_activities_by_itinerary_id(itinerary_id)
        
        return render_template("itinerary.html", itinerary=itinerary, destinations=destinations, activities=activities, API_KEY=API_KEY_FRONT)
    else:
        itinerary_name = request.form.get("name")
        overview = request.form.get("overview")

        clone_itinerary = Itinerary.clone_itinerary(original_itinerary_id=itinerary_id, 
                                user_id=session["user_id"], 
                                itinerary_name=itinerary_name, 
                                overview=overview)

        Activity.clone_activities(original_itinerary_id=itinerary_id, clone_itinerary_id=clone_itinerary.itinerary_id)

        flash(f"Success! {itinerary_name} was created.")

        return redirect(f"/itinerary/{clone_itinerary.itinerary_id}")


@app.route("/itinerary/<itinerary_id>/add_destination", methods=["POST"])
def add_destination(itinerary_id):
    """Add a destination to a travel itinerary"""

    locale = request.form.get("locale")
    territory = request.form.get("territory")
    country = request.form.get("country")
        
    itinerary = Itinerary.get_itinerary_by_itinerary_id(itinerary_id)
    location = Location.create_location(locale, territory, country)

    itinerary.locations.append(location)
    db.session.add(itinerary)
    db.session.commit()

    flash("Success! Destination added.")

    return redirect(f"/itinerary/{itinerary_id}")


@app.route("/itinerary/<itinerary_id>/delete_itinerary")
def delete_itinerary(itinerary_id):
    """Delete itinerary from database"""

    Itinerary.delete_itinerary(itinerary_id)

    flash("Success! Itinerary deleted.")

    return redirect(f"/user/{session['user']}")


@app.route("/itinerary/<itinerary_id>/search", methods=["POST", "GET"])
def search_place(itinerary_id):
    """Search for places on Google Places"""

    endpoint = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    if request.method == "POST":
        pagetoken = request.form.get("pagetoken")
        query = session["query"]
        payload = {"query": query, "pagetoken": pagetoken, "key": API_KEY}

    else:
        keyword = request.args.get("keyword", "")
        location = request.args.get("location", "")

        query = f"{keyword}+{location}"

        session["query"] = query

        payload = {"query": query, "key": API_KEY}

    response = requests.get(endpoint, params=payload)

    data = response.json()

    results = data["results"]

    photo_url = f"https://maps.googleapis.com/maps/api/place/photo?key={API_KEY}&maxheight=400&maxwidth=400&photo_reference="

    if len(results) > 0:
        return render_template("search_results.html", 
                            itinerary_id=itinerary_id, 
                            results=results, 
                            data=data,
                            photo_url=photo_url)
    else:
        flash("Search is too ambiguous. Try again.")

        return redirect(f"/itinerary/{itinerary_id}")


@app.route("/itinerary/<itinerary_id>/search/<place_id>/details", methods=["POST", "GET"])
def view_place_details(itinerary_id, place_id):
    """View details for a location on Google Places"""

    if request.method == "POST":

        try:
            formData = dict(request.form)
            place_id = formData["autocomplete"]
        except KeyError:
            flash("Place does not exist! Be sure to select an option from the available populated results.")
            return redirect(f"/itinerary/{itinerary_id}")

    endpoint = "https://maps.googleapis.com/maps/api/place/details/json"
    payload = {"place_id": place_id, "key": API_KEY}

    response = requests.get(endpoint, params=payload)

    data = response.json()

    results = data["result"]

    session["itinerary_id"] = itinerary_id

    # Store in session object to use later
    session["place_data"] = {"name": results["name"],
                            "location": results["geometry"]["location"],
                            "address": results["formatted_address"],
                            "place_url": results["url"],
                            "place_id": place_id,
                            "itinerary_id": session["itinerary_id"]}

    session["place_id"] = place_id

    return render_template("place_details.html",
                            API_KEY=API_KEY,
                            itinerary_id=itinerary_id,
                            place_id=place_id,
                            results=results)


@app.route("/itinerary/<itinerary_id>/<place_id>/add_activity")
def add_activity(itinerary_id, place_id):
    """Create an activity and add to itinerary"""

    itinerary_id = itinerary_id
    place_id = place_id

    formData = dict(request.args)

    start = formData["start"]
    end = formData["end"]
    notes = formData["notes"]

    Activity.create_activity(itinerary_id, start, end, notes, place_id)

    flash("Success! New activity added.")

    return redirect(f"/itinerary/{itinerary_id}")


@app.route("/itinerary/<itinerary_id>/edit_activity/<activity_id>", methods=["POST"])
def edit_activity(itinerary_id, activity_id):
    """Edit the logged-in user"""

    activity = Activity.get_activity_by_activity_id(activity_id)

    itinerary_id = itinerary_id

    formData = dict(request.form)
    print(formData)

    start = formData["start"]
    end = formData["end"]
    notes = formData["notes"]

    activity.edit_activity(start=start, 
                        end=end, 
                        notes=notes)
    
    flash("Activity updated!")

    return redirect(f"/itinerary/{itinerary_id}")


### API Routes  ###

@app.route("/api/itineraries/by_location")
def itineraries_by_location():
    """JSON information about itineraries by location"""

    db_itineraries_location = {}

    location_type = request.args.get("type")
    location_name = request.args.get("name")

    if location_type == "locale":
        itineraries = Itinerary.get_itinerary_by_locale(location_name)
    elif location_type == "territory":
        itineraries = Itinerary.get_itinerary_by_territory(location_name)
    elif location_type == "country":
        itineraries = Itinerary.get_itinerary_by_country(location_name)
    
    for i, itinerary in enumerate(itineraries):
        db_itineraries_location[f"{i}"] = {"itinerary_id": itinerary.itinerary_id,
                                        "itinerary_name": itinerary.itinerary_name,
        }

    return jsonify(db_itineraries_location)


@app.route("/api/itinerary_destinations")
def itinerary_destinations():
    """JSON information about all itinerary destinations for a user"""

    db_destinations = {}

    user = User.get_user_by_username(session["viewed_user"])
    itineraries = user.itineraries

    itinerary_destinations = set()

    for itinerary in itineraries:
        for location in itinerary.locations:

            destination = f"{location.locale} {location.territory} {location.country}"

            itinerary_destinations.add(destination)

    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"

    for i, destination in enumerate(itinerary_destinations):

        payload = {"address": destination, "key": API_KEY}

        response = requests.get(endpoint, params=payload)

        data = response.json()

        db_destinations[i] = data
    
    return jsonify(db_destinations)


@app.route("/api/search_place_data")
def search_place_data():
    """JSON information of a search place"""

    return jsonify(session["place_data"])


@app.route("/api/saved_activities")
def saved_place_data():
    """JSON information about previously saved activities including place_id data"""

    db_activities = {}

    activities = Activity.get_activities_by_itinerary_id(session["itinerary_id"])

    if activities == []:
        return {"success": True,
                "status": "New itinerary. No activities added yet."}
    else:

        for i, activity in enumerate(activities):

            endpoint = "https://maps.googleapis.com/maps/api/place/details/json"
            payload = {"place_id": activity.place_id, 
                        "key": API_KEY}

            response = requests.get(endpoint, params=payload)
            data = response.json()

            # print("", file=sys.stderr)
            # print(data, file=sys.stderr)
            # print("", file=sys.stderr)
            
            results = data["result"] 

            db_activities[f"{i}"] = {"activity_id": activity.activity_id,
                                    "itinerary_id": activity.itinerary_id,
                                    "dates": activity.dates,
                                    "start": activity.start,
                                    "end": activity.end,
                                    "notes": activity.notes,
                                    "place_id": activity.place_id,
                                    "results": results
            }
            
        return jsonify(db_activities)


@app.route("/api/delete_activity")
def delete_activity():
    """Delete activity from database"""

    activity_id = request.args.get("activityID")

    Activity.delete_activity(activity_id)

    return {"success": True,
            "status": "Success! Activity deleted."}


### Country Routes  ###
@app.route("/countries")
def show_countries():
    """Display Wanderlust approved countries"""

    countries = Country.get_countries()

    return render_template("countries.html", countries=countries)


if __name__ == "__main__":

    # Connect Flask app to the database
    connect_to_db(app, echo=False)

    # Connect app to the server
    app.run(host="0.0.0.0")