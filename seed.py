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
    "places": [["ChIJo15HrGUU44kREi4broJXhBE", "Flowers welcome."], ["ChIJ9_27aW8U44kRA2HY1Vk_xxQ", "Walk-in tours OK. No more than 4 people per group."], ["ChIJI_iVlmQU44kRdKHvNkSVJd0", "Dogs OK on patio."], ["ChIJYza_FmgU44kRoW-cra6Ow0Y", "Reservations required."], ["ChIJaxSbrXsU44kRlkuQDQIsixM", "Costumes welcome."]]
    },
    {"name": "Sleepless in Seattle Tour", 
    "overview": "A 5-day trip filled with delish eats, fun hikes, and lots of coffee.",
    "locale": "Seattle", 
    "territory": "Washington", 
    "country": "USA", 
    "places": [["ChIJSxh5JbJqkFQRxI1KoO7oZHs", "No photos allowed."], ["ChIJk63I_rNqkFQR3EtxoHQwzBM", "Masks required if dining indoors."], ["ChIJUX-M-a1qkFQRxtrx3nOQIKU", "Best view in Seattle."], ["ChIJ6x3yk7pqkFQRW2zXQJUlScA", "Check out the mini model of Seattle."], ["ChIJPQG7WLJqkFQRUXVHLnb3Lro", "Bring back a mug as a souvenir."]]
    },
    {"name": "Sweet Home Chicago for the Holidays", 
    "overview": "Enjoying the holidays with family and friends in back home in Chicago.",
    "locale": "Chicago", 
    "territory": "Illinois", 
    "country": "USA", 
    "places": [["ChIJh479BaAsDogRWa7hmywCQCQ", "Great spot for photos, view of the Sears Tower, and close to Lake Michigan."], ["ChIJA5xPiqYsDogRBBCptdwsGEQ", "Mandatory trip to The Bean. Also a quick walk to the Art Institute."], ["ChIJX-RTBqksDogRRh_Q4ynbf_8", "Gorgeous views and lots of places to eat or grab a drink."], ["ChIJMViM4dssDogRdmIJH2z_Q10", "Fresh pasta."], ["ChIJk6QQWKUsDogR1vrLD_bdAEc", "Wicked! Arrive 30 min before show starts."], ["ChIJKXA7AlXTD4gRsvBFJ8wG9x4", "Check out Nick Cave's Forothermore exhibit."]]
    },
    {"name": "Anniversary Trip in the City of Lights", 
    "overview": "Two romantic weeks celebrating our seventh wedding anniversary.",
    "locale": "Paris", 
    "territory": "France", 
    "country": "FRA", 
    "places": [["ChIJBxU8T_1t5kcRerSFrur9xN0", "Try the almond croissant."], ["ChIJA_6oQP5x5kcRNYQqafp0VQ4", "No children allowed."], ["ChIJe2jeNttx5kcRi_mJsGHdkQc", "Bring a hat."], ["ChIJATr1n-Fx5kcRjQb6q6cdQDY", "Walk-In Tours available."], ["ChIJD3uTd9hx5kcR1IQvGfr8dbk", "Reviews recommend at least 4 hours minimum visit to enjoy the museum. Break-up into multiple days, if possible."]]
    }
]

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

    for itinerary in itinerary_choices:

        new_itinerary = model.Itinerary.create_itinerary(user_id=user, itinerary_name=itinerary["name"], overview=itinerary["overview"])
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