"""Test data"""

import os, model, server
from random import choice
from datetime import datetime
from flask_bcrypt import Bcrypt

def connect_db():
    """Connect to the test db"""

    # Drop existing database by running dropdb command using os.system
    os.system("dropdb wanderlust")
    # Create the database by running createdb command using os.ystem
    os.system("createdb wanderlust")
    # Connect to the database
    model.connect_to_db(server.app, "postgresql:///wanderlust")
    # Create tables defined in database schema
    model.db.create_all()

def example_data():
    """Create example data for the test db"""

    users = [
        {"fname": "Ellie",
        "lname": "Wang",
        "email": "ellie.wang@gmail.com",
        "password": Bcrypt().generate_password_hash('ewang').decode('utf-8'),
        "username": "ewang",
        "locale": "Seattle",
        "territory": "Washington",
        "country": "USA",
        "about_me": "Culinary Genius \U0001F9C1 Coffee Fiend \U00002615 doggo parent \U0001F429",
        },   
        {"fname": "Katherine",
        "lname": "Nalla",
        "email": "katherine.nalla@gmail.com",
        "password": Bcrypt().generate_password_hash('knalla').decode('utf-8'),
        "username": "katherinenalla",
        "locale": "Chicago",
        "territory": "Illinois",
        "country": "USA",
        "about_me": "Traveler \U0001F30E Trekkie \U0001F596 Teacher \U0001F34E",
        }, 
        {"fname": "Andrew",
        "lname": "Lam",
        "email": "andrew.lam@gmail.com",
        "password": Bcrypt().generate_password_hash('alam').decode('utf-8'),
        "username": "andrewlam",
        "locale": "Toronto",
        "territory": "Ontario",
        "country": "CAN",
        "about_me": "I teach Brazilian Jiu-Jitsu \U0001F94B, play guitar \U0001F3B8, and like dogs \U0001F436",
        }      
    ]

    itinerary_choices = [
        {"name": ["A Wicked Halloween Weekend in Salem, Massachusetts", "A Bit of Hocus Pocus in Salem, MA", "Birthday Weekend in Salem, Mass", "Springtime in Salem", "Salem Sights & Sounds", "A Salem Summer Vacation", "Salem Retreat 2023", "Three-Day Get-Away to Salem, MA", "Exploring Salem, MA - October 2022", "Christmas in Salem"],
        "overview": "Exploring Salem, MA's historic sights and famous haunts.",
        "locale": "Salem", 
        "territory": "Massachusetts", 
        "country": "USA", 
        "places": [["ChIJo15HrGUU44kREi4broJXhBE", "Group tours available."], ["ChIJ9_27aW8U44kRA2HY1Vk_xxQ", "No more than 4 people per group."], ["ChIJI_iVlmQU44kRdKHvNkSVJd0", "Dogs OK on patio."]]
        },
        {"name": ["Sleepless in Seattle", "5 Days in Seattle - May 2024", "Bachelorette Trip to Seattle, WA", "Seattle Summer Vacation", "Seattle Trip for Two", "John & Jane's Wedding in Seattle, WA", "Seattle Food Tour", "Seattle for the Winter Holidays", "Three-Days in Seattle, Washington", "Seattle, Washington - June 2022"], 
        "overview": "A trip to Seattle filled with delish eats, fun hikes, and lots of coffee.",
        "locale": "Seattle", 
        "territory": "Washington", 
        "country": "USA", 
        "places": [["ChIJSxh5JbJqkFQRxI1KoO7oZHs", "No photos allowed."], ["ChIJk63I_rNqkFQR3EtxoHQwzBM", "Masks required if dining indoors."], ["ChIJUX-M-a1qkFQRxtrx3nOQIKU", "Best view in Seattle."]]
        },
        {"name": ["Sweet Home Chicago for the Holidays", "Adventures in Chitown", "Dharani & Amar's July Wedding in Chicago", "December 2022 Trip to Chicago for Swetha's and Amol's Wedding", "An L-evated Trip to downtown Chicago", "Whatchu talkin' about Willis Tower? June 2023 Trip to Chicago", "Chicago Stole a Pizza My Heart - Summer Trip to Chicago", "Relish the Good Times in Chicago November Trip", "CHICAGO! One Week in the Windy City", "Windy City Adventure"],
        "overview": "Three days and two nights.",
        "locale": "Chicago", 
        "territory": "Illinois", 
        "country": "USA", 
        "places": [["ChIJh479BaAsDogRWa7hmywCQCQ", "Great spot for photos, view of the Sears Tower, and close to Lake Michigan."], ["ChIJA5xPiqYsDogRBBCptdwsGEQ", "Mandatory trip to The Bean. Also a quick walk to the Art Institute."], ["ChIJX-RTBqksDogRRh_Q4ynbf_8", "Gorgeous views and lots of places to eat or grab a drink."]]
        }
    ]

    # Create users to seed the database 
    users_db = []

    for user in users:
       
        # Create User instance and add to list of users to add to database
        new_user = model.User.create_user(email=user["email"], password=user["password"], username=user["username"], fname=user["fname"], lname=user["lname"], locale=user["locale"], territory=user["territory"], country=user["country"], about_me=user["about_me"])
        users_db.append(new_user)

    # Add and commit users to the database
    model.db.session.add_all(users_db)
    model.db.session.commit()


    # To create the followers and itineraries tables, we need to get the user_id of all users in the database
    users_id = []

    all_users = model.User.get_users()

    for user in all_users:
        users_id.append(user.user_id)

    # Create followers
    followers_db = []

    for user in users_id:

        for n in range(5):

            following = choice(users_id)

            if user != following:
            
                user_followed = model.User.get_user_by_user_id(following)
                followers = user_followed.followers

                already_following = False

                for follower in followers:
                    if follower.follower_id == user:
                        already_following = True

                if not already_following:        
                    new_follower = model.Follower.create_follower(follower_id=user, user_followed_id=following)
                    followers_db.append(new_follower)    

    # Add and commit followers to the database
    model.db.session.add_all(followers_db)
    model.db.session.commit()

    start = datetime.now()
    end = datetime.utcnow()


    for user in users_id:

        itinerary = choice(itinerary_choices)

        new_itinerary = model.Itinerary.create_itinerary(user_id=user, itinerary_name=itinerary["name"][0], overview=itinerary["overview"])
        model.db.session.add(new_itinerary)
        model.db.session.commit()

        activities_db = []

        activities = itinerary["places"]

        for activity in activities:
            new_activity = model.Activity.create_activity(itinerary_id=new_itinerary.itinerary_id, 
                                            start=start,
                                            end=end,
                                            notes=activity[1],
                                            place_id=activity[0]
                                            )
            activities_db.append(new_activity)

        model.db.session.add_all(activities_db)
        model.db.session.commit()

        locale = itinerary["locale"]
        territory = itinerary["territory"]
        country = itinerary["country"]

        location = model.Location.create_location(locale=locale, territory=territory, country=country)
    
        model.db.session.add(location)
        model.db.session.commit()

        new_itinerary.locations.append(location)
        model.db.session.add(new_itinerary)
        model.db.session.commit()


    # Create Wanderlust approved countries
    countries = []

    with open("static/countrycodes.csv", "r") as f:
        for line in f:
            country = line.rstrip()
            country = country.split("|")
            countries.append(country)

    countries_db = []

    for country in countries:
        new_country = model.Country.create_country(country[0], country[1])
        countries_db.append(new_country)

    model.db.session.add_all(countries_db)
    model.db.session.commit()

def drop_db():
    """Drop test db and close session"""

    model.db.session.close()
    model.db.drop_all()