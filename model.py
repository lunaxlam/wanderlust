"""Models for Wanderlust app."""

# Import SQLAlchemy through the Flask extension
from flask_sqlalchemy import SQLAlchemy

# Create an instance of SQLAlchemy(); a db object that represents our database
db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)             # hashing when creating a User instance 
    username = db.Column(db.String(20), unique=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    current_locale = db.Column(db.String(50))
    current_territory = db.Column(db.String(50))
    current_country = db.Column(db.String(50))
    about_me = db.Column(db.Text)

    # followers = a list of Follower objects
    # travel-itineraries = a list of Travel Itinerary objects

    def __repr__(self):
        """A string representation of a User."""

        return f"<User user_id={self.user_id} username={self.username} fname={self.fname} lname={self.lname} email={self.email} >"

class Follower(db.Model):
    """A follower."""

    __tablename__ = "followers"

    follow_activity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    user_followed_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    # Establish relationship between classes
    user_to_follower = db.relationship("User", backref="followers")

    def __repr__(self):
        """A string representation of a Follower."""

        return f"<Follower follow_activity_id={self.follow_activity_id} follower_id={self.follow_id} user_followed_id={self.user_followed_id} >"

class TravelItinerary(db.Model):
    """A travel itinerary."""

    __tablename__ = "travel_itineraries"

    itinerary_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    itinerary_name = db.Column(db.String)
    overview = db.Column(db.Text)

    # itinerary_items = a list of Itinerary Item objects

    # Establish relationship between classes
    user_to_itinerary = db.relationship("User", backref="travel_itineraries")

    def __repr__(self):
        """A string representation of a Travel Itinerary."""

        return f"<Travel Itinerary itinerary_id={self.itinerary_id} itinerary_name={self.itinerary_name} user_id={self.user_id} >"

class ItineraryItem(db.Model):
    """An itinerary item."""

    __tablename__ = "itinerary_items"

    item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey("travel_itineraries.itinerary_id"))
    item_name = db.Column(db.String(50))
    date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column (db.Time)
    description = db.Column(db.Text)
    locale = db.Column(db.String)
    territory = db.Column(db.String)
    country = db.Column(db.String)
    place_id = db.Column(db.String)

    # Establish a relationship between classes
    itinerary_to_item = db.relationship("Travel Itinerary", backref="itinerary_items")

    def __repr__(self):
        "A string representation of an itineary item."

        return f"<Itinerary Item item_id={self.item_id} itinerary_id={self.itinerary_id} item_name={self.item_name} date={self.date} start_time={self.start_time} end_time={self.end_time} >"



# Set-up project
def connect_to_db(flask_app, db_name, echo=True):
    """Connect to database."""

    # Set-up database configurations
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql:///{db_name}"    # Defines the location of the database; uses default user, password, host, and port
    flask_app.config["SQLALCHEMY_ECHO"] = echo                                  # If True, we enable output of the raw SQL executed by SQLAlchemy
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False                  # Takes up a lot of memory, so set to False        

    # Connect the database with the Flask app
    db.app = flask_app
    db.init_app(flask_app)                                                      

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # To prevent SQLAlchemy from printing out every query it executes,
    # call connect_to_db(flask_app, db_name, echo=False)

    connect_to_db(app)
