"""Script to seed database."""

import os
import json
from datetime import datetime
from random import choice, randint
from faker import Faker

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


bio = ["I teach Brazilian Jiu-Jitsu, play guitar, and like dogs.",
            "Traveler \U0001F30E Trekkie \U0001F596 Teacher \U0001F34E",
            "Culinary genius, coffee fiend, doggo parent.",
            "Constantly thinking about how to Kirby-fy everything in my life.",
            "Rookie neuroscientist. \U0001F9EA \U0001F52C",
            "Millenial butterfly and make-up artist \U0001F98B \U0001F3A8",
            "Chasing moments, making memories!",
            "World traveler. Educator. Artist.",
            "Attorney, photographer, public speaker, educator",
            "Life should be enjoyed. Travel and eat!",
            "Super happy person who loves to contribute to public projects!"]

addresses = [["Chicago", "IL", "USA"], ["New York", "NY", "USA"], 
                ["Seattle", "WA", "USA"], ["Boston", "MA", "USA"], 
                ["Hong Kong Island", "Hong Kong", "HK"], ["Venice", "Veneto", "ITA"],
                ["London", "England", "UK"], ["Liverpool", "England", "UK"],
                ["Lagos", "Nigeria", "NE"], ["Taipei", "Northern Taiwan", "TAI"],
                ["Toronto", "Ontario", "CAN"], ["Calgary", "Alberta", "CAN"],
                ["Vancouver", "British Columbia", "CAN"], ["Sveta Nedelja", "Zagreb", "CI"],
                ["Odessa", "Odessa", "UKR"], ["Phom Penh", "Phnom Penh", "CAM"]]

itinerary_names = ["Sleepless in Seattle August 2022", "Sweet Home Chicago December 2022", 
                "Halloween in Salem MA October 2022", "Denver Trip May 2023",
                "Midwest Roadtrip Summer 2023", "Christmas in Toronto 2022",
                "Swetha's Birthday Weekend in Vancouver October 2022", "Eating Our Way through NYC July 2022"]


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

# Add users to the database
model.db.session.add_all(users_db)
# Commit user to the database
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

model.db.session.add_all(followers_db)
model.db.session.commit()

# Create 2 to 4 travel itineraries for each user
itineraries_db = []

for user in users_id:

    for num in range(1, randint(3, 5)):
        new_itinerary = model.Itinerary.create_itinerary(user_id=user, itinerary_name=f"{num}. {choice(itinerary_names)}", overview=fake.paragraphs(nb=3))
        itineraries_db.append(new_itinerary)

model.db.session.add_all(itineraries_db)
model.db.session.commit()

# To create the items tables, we need to get the itinerary_id of all itineraries in the database
itineraries_id = []

all_itineraries = model.Itinerary.get_itineraries()

for itinerary in all_itineraries:
    itineraries_id.append(itinerary.itinerary_id)

# Create 1 to 4 items for each itinerary:
items_db = []

for itinerary in itineraries_id:

    for num in range(1, randint(1, 5)):
        new_item = model.Item.create_item(itinerary_id=itinerary, 
                                            item_name=fake.text(max_nb_chars=50),
                                            date=fake.future_datetime(),
                                            start_time=fake.time(),
                                            end_time=fake.time(),
                                            name_or_description=fake.text(max_nb_chars=20),
                                            address=fake.address(),
                                            locale=fake.city(),
                                            territory=fake.country_code(),
                                            country=fake.country(),
                                            place_id=f"AESE8CDtyiuhjk{itinerary}")
        items_db.append(new_item)

model.db.session.add_all(items_db)
model.db.session.commit()
