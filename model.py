"""Models for Wanderlust app."""

# Import SQLAlchemy through the Flask extension
from flask_sqlalchemy import SQLAlchemy

# Create an instance of SQLAlchemy(); a db object that represents our database
db = SQLAlchemy()



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
