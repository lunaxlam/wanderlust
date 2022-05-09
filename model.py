"""Models for Wanderlust app."""

# Import SQLAlchemy through the Flask extension
from flask_sqlalchemy import SQLAlchemy

# Constructor function to create an instance of SQLAlchemy; a db object that represents our database
# The db object can use SQLAlchemy class methods like db.create_all(), .add(), .commit()
db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)                             # hashing when creating a User instance 
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

        return f"<User user_id={self.user_id} username={self.username} fname={self.fname} lname={self.lname} email={self.email} >"

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

        return db.session.query(User)

    @classmethod
    def get_user_by_username(cls, username):
        """Return a user by username"""

        return User.query.filter(User.username == username).first()
    
    @classmethod
    def get_user_by_email(cls, email):
        """Return a user by email"""

        return User.query.filter(User.email == email).first()


class Follower(db.Model):
    """A Follower."""

    __tablename__ = "followers"

    activity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey("users.user_id")) # lender_id
    user_followed_id = db.Column(db.Integer, db.ForeignKey("users.user_id")) #seller_id

    # Establish relationship between classes; stores a User object associated with the defined foreign_key value
    follower = db.relationship("User", foreign_keys=[follower_id], backref="followers") 
    user_followed = db.relationship("User", foreign_keys=[user_followed_id], backref="users_followed") 

    def __repr__(self):
        """A string representation of a Follower."""

        return f"<Follower activity_id={self.activity_id} follower_id={self.follower_id} follower={self.follower.username} user_followed_id={self.user_followed_id} user_followed={self.user_followed.username}>"

    @classmethod
    def create_follower(cls, follower_id, user_followed_id):
        """Create and return a follower"""

        follower = Follower(follower_id=follower_id,
                            user_followed_id=user_followed_id)
        
        return follower
    
    @classmethod
    def get_followers(cls):
        """Return all follower objects"""

        return db.session.query(Follower)

    @classmethod
    def get_follower_by_follower_id(cls, follower_id):
        """Return a follower by follower_id"""

        return Follower.query.filter(Follower.follower_id == follower_id).first()

    @classmethod
    def get_followers_by_user_followed_id(cls, user_followed_id):
        """Return all followers that are following a specified user_followed_id"""

        return Follower.query.filter(Follower.user_followed_id == user_followed_id).all()

    @classmethod
    def get_following_by_follower_id(cls, follower_id):
        """Return all followers that are being followed by a specified follower_id"""

        return Follower.query.filter(Follower.follower_id == follower_id).all()


class Itinerary(db.Model):
    """A travel itinerary."""

    __tablename__ = "itineraries"

    itinerary_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    itinerary_name = db.Column(db.String, nullable=False)
    overview = db.Column(db.Text, nullable=False)
    locale = db.Column(db.String, nullable=False)
    territory = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)

    # activities = a list of itinerary Activity objects

    # Establish relationship between Itinerary class and User class
    user = db.relationship("User", backref="itineraries")

    def __repr__(self):
        """A string representation of a travel itinerary."""

        return f"<Itinerary itinerary_id={self.itinerary_id} itinerary_name={self.itinerary_name} user_id={self.user_id} >"
    
    @classmethod
    def create_itinerary(cls, user_id, itinerary_name, overview, locale, territory, country):

        itinerary_name = itinerary_name.title()
        locale = locale.title()
        territory = territory.title()
        country = country.upper()
        
        itinerary = Itinerary(user_id=user_id,
                                itinerary_name=itinerary_name,
                                overview=overview,
                                locale=locale,
                                territory=territory,
                                country=country)
        
        return itinerary

    @classmethod
    def get_itineraries(cls):
        """Return all itinerary objects"""

        return db.session.query(Itinerary)

    @classmethod
    def get_itinerary_by_itinerary_id(cls, itinerary_id):
        """Return an itinerary by itinerary_id"""

        return Itinerary.query.filter(Itinerary.itinerary_id == itinerary_id).first()

    @classmethod
    def get_itinerary_by_user_id(cls, user_id):
        """Return all itineraries by user_id"""

        return Itinerary.query.filter(Itinerary.user_id == user_id).all()


class Activity(db.Model):
    """An itinerary activity item."""

    __tablename__ = "activities"

    activity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey("itineraries.itinerary_id"))
    activity_name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.String, nullable=True)
    end_time = db.Column (db.String, nullable=True)
    place_id = db.Column(db.String, nullable=False)

    # Establish a relationship between Item class and Itinerary class
    itinerary = db.relationship("Itinerary", backref="activities")

    def __repr__(self):
        "A string representation of an itineary item."

        return f"<Activity activity_id={self.activity_id} itinerary_id={self.itinerary_id} activity_name={self.activity_name} date={self.date} start_time={self.start_time} end_time={self.end_time} >"

    @classmethod
    def create_activity(cls, itinerary_id, activity_name, date, start_time, end_time, place_id):
        
        activity_name = activity_name.title()

        activity = Activity(itinerary_id=itinerary_id,
                    activity_name=activity_name,
                    date=date,
                    start_time=start_time,
                    end_time=end_time,
                    place_id=place_id)
        
        return activity
    
    @classmethod
    def get_activities(cls):
        """Return all itinerary activity item objects"""

        return db.session.query(Activity)

    @classmethod
    def get_activity_by_itinerary_id(cls, itinerary_id):
        """Return all items by itinerary_id"""

        return Activity.query.filter(Activity.itinerary_id == itinerary_id).all()


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