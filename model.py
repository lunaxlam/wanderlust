"""Models for Wanderlust app"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Constructor function to create an instance of SQLAlchemy; a db object that represents our database
# The db object can use SQLAlchemy class methods like db.create_all(), .add(), .commit()
db = SQLAlchemy()

class User(db.Model):
    """A user"""

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
        """A string representation of a User"""

        return f"<User user_id={self.user_id} username={self.username} email={self.email} locale={self.locale} territory={self.territory} country={self.country}>"

    @classmethod
    def create_user(cls, email, password, username, fname, lname, locale, territory, country, about_me):
        """Create and return a new user"""

        email = email.lower()
        username = username.lower()
        fname = fname.title()
        lname = lname.title()
        locale = locale.title()
        territory = territory.title()
        country = country.upper()

        user = cls(email=email, 
                    password=password, 
                    username=username, 
                    fname=fname, 
                    lname=lname, 
                    locale=locale, 
                    territory=territory, 
                    country=country, 
                    about_me=about_me)
        
        db.session.add(user)
        db.session.commit()
        
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
    """A Follower"""

    __tablename__ = "followers"

    follow_activity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    user_followed_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    # Establish relationship between classes; stores a User object associated with the defined foreign_key value
    follower = db.relationship("User", foreign_keys=[follower_id], backref="following") 
    user_followed = db.relationship("User", foreign_keys=[user_followed_id], backref="followers") 

    def __repr__(self):
        """A string representation of a Follower"""

        return f"<Follower follow_activity_id={self.follow_activity_id} follower_id={self.follower_id} follower={self.follower.username} user_followed_id={self.user_followed_id} user_followed={self.user_followed.username}>"

    @classmethod
    def create_follower(cls, follower_id, user_followed_id):
        """Create and return a follower"""

        follower = cls(follower_id=follower_id, user_followed_id=user_followed_id)

        db.session.add(follower)
        db.session.commit()
        
        return follower
    
    @classmethod
    def get_followers(cls):
        """Return all follower objects"""

        return cls.query


class Itinerary(db.Model):
    """A travel itinerary"""

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
        """A string representation of a travel itinerary"""

        return f"<Itinerary itinerary_id={self.itinerary_id} itinerary_name={self.itinerary_name} user_id={self.user_id} locations={self.locations}>"
    
    @classmethod
    def create_itinerary(cls, user_id, itinerary_name, overview):
        """Create and return an itinerary"""
        
        itinerary = cls(user_id=user_id, itinerary_name=itinerary_name, overview=overview)
        db.session.add(itinerary)
        db.session.commit()
        
        return itinerary

    @classmethod
    def clone_itinerary(cls, original_itinerary_id, user_id, itinerary_name, overview):
        """Clone an itinerary"""

        clone_itinerary = cls.create_itinerary(user_id, itinerary_name, overview)

        db.session.add(clone_itinerary)
        db.session.commit()

        original_itinerary = cls.get_itinerary_by_itinerary_id(original_itinerary_id)
        destinations = original_itinerary.locations

        for destination in destinations:
            clone_itinerary.locations.append(destination)
    
        db.session.add(clone_itinerary)
        db.session.commit()

        return clone_itinerary

    @classmethod
    def delete_itinerary(cls, itinerary_id):
        """Delete itinerary from database"""

        itinerary = cls.query.filter_by(itinerary_id=itinerary_id).first()
        
        db.session.delete(itinerary)
        db.session.commit()

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
    """An itinerary activity item"""

    __tablename__ = "activities"

    activity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey("itineraries.itinerary_id"))
    dates = db.Column(db.String, nullable=True)
    start = db.Column(db.String, nullable=True)
    end = db.Column (db.String, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    place_id = db.Column(db.String, nullable=False)

    # Establish a relationship between Item class and Itinerary class
    itinerary = db.relationship("Itinerary", backref="activities")

    def __repr__(self):
        "A string representation of an itineary activity item"

        return f"<Activity activity_id={self.activity_id} itinerary_id={self.itinerary_id} start={self.start} end_time={self.end}>"

    @classmethod
    def create_activity(cls, itinerary_id, start, end, notes, place_id):
        """Create and return an itinerary activity item"""

        # Convert string-datetime into datetime object
        if isinstance(start, str) and isinstance(end, str):
            start = datetime.strptime(start, "%Y-%m-%dT%H:%M")
            end = datetime.strptime(end, "%Y-%m-%dT%H:%M")

        # Update string output of datetime object
        start_time = start.strftime("%-I:%M %p")
        end_time = end.strftime("%-I:%M %p")

        # Set string output of datetime object to locale representation
        start_date = start.strftime("%x %Z")
        end_date = end.strftime("%x %Z")

        if start_date != end_date:
            dates = f"{start_date} to {end_date}"
            start_time = f"{start_time} on {start_date}"
            end_time = f"{end_time} on {end_date}"
        else:
            dates = start_date
 
        activity = cls(itinerary_id=itinerary_id,
                    dates=dates,
                    start=start_time,
                    end=end_time,
                    notes=notes,
                    place_id=place_id)
        
        db.session.add(activity)
        db.session.commit()
        
        return activity
    
    @classmethod
    def clone_activities(cls, original_itinerary_id, clone_itinerary_id):
        """Clone activities from database"""

        activities = cls.get_activities_by_itinerary_id(original_itinerary_id)

        for activity in activities:
            clone_activity = cls(itinerary_id=clone_itinerary_id,
                                    dates=activity.dates,
                                    start=activity.start,
                                    end=activity.end,
                                    notes=activity.notes,
                                    place_id=activity.place_id)
            
            db.session.add(clone_activity)
        
        db.session.commit()

    @classmethod
    def delete_activity(cls, activity_id):
        """Delete activity from database"""

        activity = cls.query.filter_by(activity_id=activity_id).first()
        
        db.session.delete(activity)
        db.session.commit()
    
    @classmethod
    def get_activities(cls):
        """Return all itinerary activity items"""

        return cls.query
    
    @classmethod
    def get_activities_by_itinerary_id(cls, itinerary_id):
        """Return all itinerary activity items by itinerary_id"""

        return cls.query.filter(cls.itinerary_id == itinerary_id).all()


class Location(db.Model):
    """A location"""

    __tablename__ = "locations"

    location_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    locale = db.Column(db.String(50), nullable=False)
    territory = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        "A string representation of a Location item"

        return f"<Location location_id={self.location_id} locale={self.locale} territory={self.territory} country={self.country}>"

    @classmethod
    def create_location(cls, locale, territory, country):
        """Create and return a location"""
        
        locale = locale.title()
        territory = territory.title()
        country = country.upper()

        location = cls(locale=locale, territory=territory, country=country)

        db.session.add(location)
        db.session.commit()
        
        return location
    
    @classmethod
    def get_locations(cls):
        """Return all Location objects"""

        return cls.query


class Destination(db.Model):
    """An association table between Itinerary and Location"""

    __tablename__ = "destinations"

    destination_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey("itineraries.itinerary_id"), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.location_id"), nullable=False)

    def __repr__(self):
        "A string representation of a destination location item"

        return f"<Destination destination_id={self.destination_id} itinerary_id={self.itinerary_id} location_id={self.location_id}>"


class Country(db.Model):
    """A country"""

    __tablename__ = "countries"

    code_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    country_code = db.Column(db.String(3), nullable=False)
    country_name = db.Column(db.String, nullable=False)

    def __repr__(self):
        "A string representation of a country"

        return f"<Country id={self.code_id} name={self.country_name} code={self.country_code}>"
    
    @classmethod
    def create_country(cls, country_code, country_name):
        """Create and return a country"""

        country = cls(country_code=country_code, country_name=country_name)

        return country

    @classmethod
    def get_countries(cls):
        """Return all countries"""

        return cls.query


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