"""Script to seed database"""

import os
from random import choice, randint
from faker import Faker

import model
import server

from datetime import datetime


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

addresses = [["Chicago", "Illinois", "USA"], ["New York", "New York", "USA"], 
                ["Seattle", "Washington", "USA"], ["Boston", "Massachusetts", "USA"], 
                ["Hong Kong Island", "Hong Kong", "HK"], ["Venice", "Veneto", "ITA"],
                ["London", "England", "UK"], ["Liverpool", "England", "UK"],
                ["Lagos", "Nigeria", "NE"], ["Taipei", "Northern Taiwan", "TAI"],
                ["Toronto", "Ontario", "CAN"], ["Calgary", "Alberta", "CAN"],
                ["Vancouver", "British Columbia", "CAN"], ["Sveta Nedelja", "Zagreb", "CI"],
                ["Odessa", "Odessa", "UKR"], ["Phnom Penh", "Phnom Penh", "CAM"]]

itinerary_names = [f"Summer Vacation {randint(2022, 2030)}", f"Home for the Holidays {randint(2022, 2030)}", 
                f"A Screaming Halloween Weekend", f"May Adventures {randint(2022, 2030)}",
                f"Summer Road Trip {randint(2022, 2030)}", f"Anniversary Trip {randint(2022, 2030)}",
                f"Labor Day Weekend {randint(2022, 2030)}", f"Wedding Season {randint(2022, 2030)}"]

notes = ["Reservations up to 24 hours in advance", "No cell phones", "BYOB is ok",
        "21+ only", "No children under 12 yrs",  "Face masks required",
        "Dogs OK", "Limited outdoor seating", "Patio closed for the season"]

place_ids = ["ChIJaXQRs6lZwokRY6EFpJnhNNE"]

# Create users to seed the database 
users_db = []

for n in range (20):
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

# Create followers
followers_db = []

for n in range(50):
    follower_id = choice(users_id)
    user_followed_id = choice(users_id)

    if follower_id != user_followed_id:
        new_follower = model.Follower.create_follower(follower_id, user_followed_id)
        followers_db.append(new_follower)

# Add and commit followers to the database
model.db.session.add_all(followers_db)
model.db.session.commit()


# Create a few travel itineraries for each user
itineraries_db = []

for user in users_id:

    for num in range(randint(5, 6)):
        new_itinerary = model.Itinerary.create_itinerary(user_id=user, itinerary_name=f"{choice(itinerary_names)}", overview="The greatest trip ever planned.")
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

# Create a few activity items for each itinerary:
activities_db = []

for itinerary in itineraries_id:

    start = datetime.now()
    end = datetime.utcnow()

    for num in range(randint(3, 5)):
        new_activity = model.Activity.create_activity(itinerary_id=itinerary, 
                                            activity_name="A Super Fun Activity Name",
                                            start=start,
                                            end=end,
                                            notes=choice(notes),
                                            place_id=choice(place_ids)
                                            )
        activities_db.append(new_activity)

# Add and commit activities to the database
model.db.session.add_all(activities_db)
model.db.session.commit()


# Create locations
locations = []

for address in addresses:
    locale = address[-3]
    territory = address[-2]
    country = address[-1]

    location = [locale, territory, country]
    
    locations.append(location)


# Add locations to itineraries
for itinerary in all_itineraries:

    location  = choice(locations)

    location = model.Location.create_location(locale=location[0], territory=location[1], country=location[2])
    
    model.db.session.add(location)
    model.db.session.commit()

    itinerary.locations.append(location)
    model.db.session.add(itinerary)

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