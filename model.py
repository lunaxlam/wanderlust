"""Models for Wanderlust app"""

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

# Constructor function to create an instance of SQLAlchemy; a db object that represents our database
# The db object can use SQLAlchemy class methods like db.create_all(), .add(), .commit()
db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)                        #### !!! Sprint 2: hashing and salting when creating a User instance 
    username = db.Column(db.String(20), nullable=False, unique=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    locale = db.Column(db.String(50), nullable=False)
    territory = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    about_me = db.Column(db.Text, nullable=True)

    # followers = a list of Follower objects that are following a user; use User.query.filter(User.followers).all(), for example
    # users_followed = a list of Follower objects that are users being followed; use User.query.filter(User.users_followed).all(), for example
    # itineraries = a list of Itinerary objects

    def __repr__(self):
        """A string representation of a User."""

        return f"<User user_id={self.user_id} username={self.username} email={self.email} locale={self.locale} territory={self.territory} country={self.country}>"

    @classmethod
    def create_user(cls, email, password, username, fname, lname, locale, territory, country, about_me):
        """Create and return a new user"""

        email = email.lower()
        username = username.lower()
        fname = fname.title()
        lname = lname.title()
        locale = locale.lower()
        territory = territory.lower()
        country = country.lower()

        user = User(email=email, 
                    password=password, 
                    username=username, 
                    fname=fname, 
                    lname=lname, 
                    locale=locale, 
                    territory=territory, 
                    country=country, 
                    about_me=about_me)
        
        return user

    @classmethod
    def get_users(cls):
        """Return all user objects"""

        return cls.query

    @classmethod
    def get_user_by_username(cls, username):
        """Return a user object by username"""

        return cls.query.filter(cls.username == username).first()
    
    @classmethod
    def get_user_by_email(cls, email):
        """Return a user object by email"""

        return cls.query.filter(cls.email == email).first()    

    @classmethod
    def get_user_by_locale(cls, locale):
        """Returns a list of all users by locale"""

        return cls.query.filter(cls.locale == locale).all()
    
    @classmethod
    def get_user_by_territory(cls, territory):
        """Returns a list of all users by territory"""

        return cls.query.filter(cls.territory == territory).all()
    
    @classmethod
    def get_user_by_country(cls, country):
        """Returns a list of all users by country"""

        return cls.query.filter(cls.country == country).all()


class Follower(db.Model):
    """A Follower."""

    __tablename__ = "followers"

    follow_activity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    user_followed_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    # Establish relationship between classes; stores a User object associated with the defined foreign_key value
    follower = db.relationship("User", foreign_keys=[follower_id], backref="following") 
    user_followed = db.relationship("User", foreign_keys=[user_followed_id], backref="followers") 

    def __repr__(self):
        """A string representation of a Follower."""

        return f"<Follower follow_activity_id={self.follow_activity_id} follower_id={self.follower_id} follower={self.follower.username} user_followed_id={self.user_followed_id} user_followed={self.user_followed.username}>"

    @classmethod
    def create_follower(cls, follower_id, user_followed_id):
        """Create and return a follower"""

        follower = Follower(follower_id=follower_id, user_followed_id=user_followed_id)
        
        return follower
    
    @classmethod
    def get_followers(cls):
        """Return all follower objects"""

        return cls.query


class Itinerary(db.Model):
    """A travel itinerary."""

    __tablename__ = "itineraries"

    itinerary_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    itinerary_name = db.Column(db.String, nullable=False)
    overview = db.Column(db.Text, nullable=False)

    # Establish relationship between Itinerary class and User class
    user = db.relationship("User", backref="itineraries")
    
    # Establish relationship with the Association table
    locations = db.relationship("Location", secondary="destinations", backref="itineraries")

    # activities = a list of itinerary Activity objects

    def __repr__(self):
        """A string representation of a travel itinerary."""

        return f"<Itinerary itinerary_id={self.itinerary_id} itinerary_name={self.itinerary_name} user_id={self.user_id} locations={self.locations}>"
    
    @classmethod
    def create_itinerary(cls, user_id, itinerary_name, overview):
        
        itinerary = Itinerary(user_id=user_id, itinerary_name=itinerary_name, overview=overview)
        
        return itinerary

    @classmethod
    def get_itineraries(cls):
        """Return all itinerary objects"""

        return cls.query

    @classmethod
    def get_itinerary_by_itinerary_id(cls, itinerary_id):
        """Return an itinerary object by itinerary_id"""

        return cls.query.filter(cls.itinerary_id == itinerary_id).first()
    
    @classmethod
    def get_itinerary_by_locale(cls, locale):
        """Return a list of all itineraries by location locale"""

        return cls.query.join(cls.locations).filter(Location.locale == locale).all()

    @classmethod
    def get_itinerary_by_territory(cls, territory):
        """Return a list of all itineraries by location territory"""

        return cls.query.join(cls.locations).filter(Location.territory == territory).all()
    
    @classmethod
    def get_itinerary_by_country(cls, country):
        """Return a list of all itineraries by location country"""

        return cls.query.join(cls.locations).filter(Location.country == country).all()


class Activity(db.Model):
    """An itinerary activity item."""

    __tablename__ = "activities"

    activity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey("itineraries.itinerary_id"))
    activity_name = db.Column(db.String(50), nullable=False)
    start = db.Column(db.String, nullable=True)
    end = db.Column (db.String, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    place_id = db.Column(db.String, nullable=False)

    # Establish a relationship between Item class and Itinerary class
    itinerary = db.relationship("Itinerary", backref="activities")

    def __repr__(self):
        "A string representation of an itineary item."

        return f"<Activity activity_id={self.activity_id} itinerary_id={self.itinerary_id} activity_name={self.activity_name} start={self.start} end_time={self.end}>"

    @classmethod
    def create_activity(cls, itinerary_id, activity_name, start, end, notes, place_id):
        
        activity_name = activity_name.title()

        if isinstance(start, str) and isinstance(end, str):
            start = datetime.strptime(start, "%Y-%m-%dT%H:%M")
            end = datetime.strptime(end, "%Y-%m-%dT%H:%M")

        start = start.strftime("%A, %B %-m, %Y - %-I:%M %p")
        end = end.strftime("%A, %B %-m, %Y - %-I:%M %p")

        activity = Activity(itinerary_id=itinerary_id,
                    activity_name=activity_name,
                    start=start,
                    end=end,
                    notes=notes,
                    place_id=place_id)
        
        return activity
    
    @classmethod
    def get_activities(cls):
        """Return all itinerary activity items"""

        return cls.query
    
    @classmethod
    def get_activities_by_itinerary_id(cls, itinerary_id):
        """Return all itinerary activity items by itinerary_id"""

        return cls.query.filter(cls.itinerary_id == itinerary_id).all()


class Location(db.Model):
    """A location."""

    __tablename__ = "locations"

    location_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    locale = db.Column(db.String(50), nullable=False)
    territory = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        "A string representation of a Location item."

        return f"<Location location_id={self.location_id} locale={self.locale} territory={self.territory} country={self.country}>"

    @classmethod
    def create_location(cls, locale, territory, country):
        
        locale = locale.lower()
        territory = territory.lower()
        country = country.lower()

        location = Location(locale=locale, territory=territory, country=country)
        
        return location
    
    @classmethod
    def get_locations(cls):
        """Return all Location objects"""

        return cls.query


class Destination(db.Model):
    """An association table between Itinerary and Location."""

    __tablename__ = "destinations"

    destination_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey("itineraries.itinerary_id"), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.location_id"), nullable=False)

    def __repr__(self):
        "A string representation of a destination location item."

        return f"<Destination destination_id={self.destination_id} itinerary_id={self.itinerary_id} location_id={self.location_id}>"


# Set-up project to connect SQLAlchemy to Postgres database; this is done through psycopg2
def connect_to_db(flask_app, db_uri="postgresql:///wanderlust", echo=True):
    """Connect Flask app to database."""

    # Set-up database configurations
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri    # Defines the location of the database; uses default user, password, host, and port
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