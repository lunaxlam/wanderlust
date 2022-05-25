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
                ["Hong Kong Island", "Hong Kong", "HKG"], ["Venice", "Veneto", "ITA"],
                ["London", "England", "GBR"], ["Liverpool", "England", "GBR"],
                ["Lagos", "Nigeria", "NGA"], ["Taipei", "Northern Taiwan", "TAI"],
                ["Toronto", "Ontario", "CAN"], ["Calgary", "Alberta", "CAN"],
                ["Vancouver", "British Columbia", "CAN"], ["Sveta Nedelja", "Zagreb", "HRV"],
                ["Odessa", "Odessa", "UKR"], ["Phnom Penh", "Phnom Penh", "CAM"]]

itinerary_choices = [
    {"name": "A Screaming Halloween Weekend in Salem",
    "overview": "Three-day weekend exploring historic sights and famous haunts.",
    "locale": "Salem", 
    "territory": "Massachusetts", 
    "country": "USA", 
    "places": ["ChIJId0s1WQU44kRHgLHTfrQHc4", "ChIJ9_27aW8U44kRA2HY1Vk_xxQ", "ChIJ7XbB2HoU44kRl7_QkmUYukc", "ChIJr6C08etv5IkRAyk-rB7uevo"]
    },
    {"name": "Sleepless in Seattle Tour", 
    "overview": "A 5-day trip filled with delish eats, fun hikes, and lots of coffee.",
    "locale": "Seattle", 
    "territory": "Washington", 
    "country": "USA", 
    "places": ["ChIJ7ZC5oTcVkFQR4tJqYR-hWbU", "ChIJPQG7WLJqkFQRUXVHLnb3Lro", "ChIJk63I_rNqkFQR3EtxoHQwzBM", "ChIJb6RGGMJrkFQRrLOGJZumVwM"]
    },
    {"name": "Sweet Home Chicago for the Holidays", 
    "overview": "Enjoying the holidays with family and friends in back home in Chicago.",
    "locale": "Chicago", 
    "territory": "Illinois", 
    "country": "USA", 
    "places": ["ChIJoToyIa4sDogROtxPMF-6QN8-hWbU", "ChIJNbKQElTTD4gRREaOJN5ZUdw", "ChIJici8qWgsDogRuoxl5U7xq7g", "ChIJFR3zFUHTD4gRiSGHi3J4B7Y"]
    },
    {"name": "Taking 5 in the 5 Boroughs", 
    "overview": "A 5-day trip in the concrete jungle.",
    "locale": "New York", 
    "territory": "New York", 
    "country": "USA", 
    "places": ["ChIJg5jn8FNYwokRwH-6QN8-hWbU", "ChIJbz1TL6ZZwokRv_VvWdOElb0", "ChIJ5bQPhMdZwokRkTwKhVxhP1g", "ChIJLWBE3YNZwokRh2EBs1QXfzM"]
    },
    {"name": "A Hong Kong Summer", 
    "overview": "14 days in the 852",
    "locale": "Hong Kong", 
    "territory": "Hong Kong", 
    "country": "HKG", 
    "places": ["ChIJn-mOoECqBjQRJssZ2P6yqKA", "ChIJnz5FoVAABDQR6OQrQ1dEduk", "ChIJwzeIKmUABDQR8VxjuNzFq3Q", "ChIJM5NtTLwFBDQR"]
    },
    {"name": "A Spring Get-Away to London", 
    "overview": "Care for more tea? 5 days and 4 nights enjoying adventures across the pond.",
    "locale": "London", 
    "territory": "England", 
    "country": "GBR", 
    "places": ["ChIJx5m01ssEdkgRU", "ChIJH4s0zCshe0gRf2E8UP9JbVY", "ChIJtwn55ikFdkgRAvOuPIWeLM0", "ChIJuXRc9xcxY0gRwGQcQqfm5j4"]
    },
    {"name": "Anniversary Trip in the City of Lights", 
    "overview": "Two romantic weeks celebrating our seventh wedding anniversary.",
    "locale": "Paris", 
    "territory": "France", 
    "country": "FRA", 
    "places": ["ChIJA_6oQP5x5kcRNYQqafp0VQ4", "ChIJLU7jZClu5kcR4PcOOO6p3I0", "ChIJBxU8T_1t5kcRerSFrur9xN0", "ChIJryei4kRu5kcRgmdcbzUwGWQ"]
    },
    {"name": "Two-Days in Door County", 
    "overview": "A great weekend get away to Door County, Wisconsin",
    "locale": "Door County", 
    "territory": "Michigan", 
    "country": "USA", 
    "places": ["ChIJM_bkgNNMTU0RtV8SwtzQppM", "ChIJdwCTU6QcTU0RxX7hCpB_7Cw", "ChIJdaQyeQhQHYgRwtTTevJKh0w", "ChIJ9UqquOlHTU0RPXCugSNZmwo"]
    }
]

notes = ["Reservations up to 24 hours in advance", "No cell phones", "BYOB is ok",
        "21+ only", "No children under 12 yrs",  "Face masks required",
        "Dogs OK", "Limited outdoor seating", "Patio closed for the season"]

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

start = datetime.now()
end = datetime.utcnow()

for user in users_id:

    for num in range(randint(2, 4)):

        itinerary = choice(itinerary_choices)

        new_itinerary = model.Itinerary.create_itinerary(user_id=user, itinerary_name=itinerary["name"], overview=itinerary["overview"])
        model.db.session.add(new_itinerary)
        model.db.session.commit()

        activities_db = []

        for num in range(randint(2, 4)):
            new_activity = model.Activity.create_activity(itinerary_id=new_itinerary.itinerary_id, 
                                            activity_name="A Super Fun Activity",
                                            start=start,
                                            end=end,
                                            notes=choice(notes),
                                            place_id=choice(itinerary["places"])
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