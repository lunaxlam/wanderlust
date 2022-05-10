"""Script to seed database."""

import os
import json
from random import choice, randint
from faker import Faker
import requests

import model
import server


# Drop existing database by running dropdb command using os.system
os.system("dropdb wanderlust")
# Create the database by running createdb command using os.ystem
os.system("createdb wanderlust")
# Connect to the database
model.connect_to_db(server.app)
# Create tables defined in database schema
model.db.create_all()

# Create an instance of a faker generator to generate data
fake = Faker()


bio = ["I teach Brazilian Jiu-Jitsu \U0001F94B, play guitar \U0001F3B8, and like dogs \U0001F436",
            "Traveler \U0001F30E Trekkie \U0001F596 Teacher \U0001F34E",
            "Culinary Genius \U0001F9C1 Coffee Fiend \U00002615 doggo parent \U0001F429",
            "Constantly thinking about how to Kirby-fy everything in my life \U0001F3AE",
            "Rookie neuroscientist. \U0001F9EA \U0001F52C",
            "Millenial butterfly and make-up artist \U0001F98B \U0001F3A8",
            "Chasing moments, making memories! \U0001F60E",
            "World traveler \U0001F30F Educator \U0001F34E Artist \U0001F3A8",
            "Photographer \U0001F4F7 Public Speaker \U0001F3A4 Educator \U0001F34E",
            "Life should be enjoyed. Travel and eat! \U0001F5FA \U0001F9CB"]

addresses = [["Chicago", "IL", "USA"], ["New York", "NY", "USA"], 
                ["Seattle", "WA", "USA"], ["Boston", "MA", "USA"], 
                ["Hong Kong Island", "Hong Kong", "HK"], ["Venice", "Veneto", "ITA"],
                ["London", "England", "UK"], ["Liverpool", "England", "UK"],
                ["Lagos", "Nigeria", "NE"], ["Taipei", "Northern Taiwan", "TAI"],
                ["Toronto", "Ontario", "CAN"], ["Calgary", "Alberta", "CAN"],
                ["Vancouver", "British Columbia", "CAN"], ["Sveta Nedelja", "Zagreb", "CI"],
                ["Odessa", "Odessa", "UKR"], ["Phnom Penh", "Phnom Penh", "CAM"]]

itinerary_names = [f"Sleepless in Seattle August {randint(2022, 2030)}", f"Sweet Home Chicago December {randint(2022, 2030)}", 
                f"Halloween in Salem MA October {randint(2022, 2030)}", f"Denver Trip May {randint(2022, 2030)}",
                f"Midwest Roadtrip Summer {randint(2022, 2030)}", f"Christmas in Toronto {randint(2022, 2030)}",
                f"Louis Birthday Weekend September {randint(2022, 2030)}", f"Eating Our Way through NYC July {randint(2022, 2030)}"]


# Create 25 users to seed the database 
users_db = []

for n in range (25):
    fname = fake.unique.first_name()
    lname = fake.unique.last_name()
    domain = fake.free_email_domain()
    email = f'{fname}.{lname}@{domain}'
    password = "password123"
    username = f'{fname}{lname}'
    address = choice(addresses)
    locale = address[-3]
    territory = address[-2]
    country = address[-1]
    about_me = choice(bio)

    # Create User instance and add to list of users to add to database
    new_user = model.User.create_user(email, password, username, fname, lname, locale, territory, country, about_me)
    users_db.append(new_user)

# Add and commit users to the database
model.db.session.add_all(users_db)
model.db.session.commit()


# To create the followers and itineraries tables, we need to get the user_id of all users in the database
users_id = []

all_users = model.User.get_users()

for user in all_users:
    users_id.append(user.user_id)

# Create 40 followers
followers_db = []

for n in range(40):
    follower_id = choice(users_id)
    user_followed_id = choice(users_id)

    if follower_id != user_followed_id:
        new_follower = model.Follower.create_follower(follower_id, user_followed_id)
        followers_db.append(new_follower)

# Add and commit followers to the database
model.db.session.add_all(followers_db)
model.db.session.commit()


# Create 2 to 4 travel itineraries for each user
itineraries_db = []

for user in users_id:

    for num in range(1, randint(3, 5)):
        new_itinerary = model.Itinerary.create_itinerary(user_id=user, itinerary_name=f"{num}. {choice(itinerary_names)}", overview=fake.text(max_nb_chars=50))
        itineraries_db.append(new_itinerary)

# Add and commit itineraries to the database
model.db.session.add_all(itineraries_db)
model.db.session.commit()


# To create activities for each itinerary, we will need the itinerary_id
itineraries_id = []

# To access the itinerary_id and also to create locations for each itinerary, get all itineraries
all_itineraries = model.Itinerary.get_itineraries()

for itinerary in all_itineraries:
    itineraries_id.append(itinerary.itinerary_id)

# Create 2 to 4 activity items for each itinerary:
activities_db = []

for itinerary in itineraries_id:

    for num in range(1, randint(3, 5)):
        new_activity = model.Activity.create_activity(itinerary_id=itinerary, 
                                            activity_name="Dinner at Cotogna",
                                            date=fake.future_datetime(),
                                            start_time=fake.time(),
                                            end_time=fake.time(),
                                            notes=fake.text(max_nb_chars=50),
                                            place_id=f"ChIJA0YvGPWAhYAReXmaDTTdWzU")
        activities_db.append(new_activity)

# Add and commit activities to the database
model.db.session.add_all(activities_db)
model.db.session.commit()


# Create locations
locations_db = []

for address in addresses:
    locale = address[-3]
    territory = address[-2]
    country = address[-1]

    location = model.Location.create_location(locale=locale, territory=territory, country=country)

    locations_db.append(location)

model.db.session.add_all(locations_db)
model.db.session.commit()


# Create 2 to 4 locations for each itinerary
all_locations = model.Location.get_locations().all()

for itinerary in all_itineraries:

    for num in range(1, randint(3, 5)):
        location  = choice(all_locations)

        itinerary.locations.append(location)
        model.db.session.add(itinerary)

model.db.session.commit()