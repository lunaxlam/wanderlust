"""Script to seed database"""

import os, model, server
from random import choice
from faker import Faker
from datetime import datetime
from flask_bcrypt import Bcrypt


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

first_names = ["Taylor", "Alex", "Kennedy", "Jordan", "Brooklyn", "Parker", "Charlie", "Rowan", "Harley", "Blake"]

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
    {"name": ["A Wicked Halloween Weekend in Salem, Massachusetts", "Enjoying a Bit of Hocus Pocus in Salem, MA", "Birthday Weekend in Salem, Mass", "Springtime in Salem", "Salem Sights & Sounds", "A Salem Summer Vacation", "Salem Retreat 2023", "Three-Day Get-Away to Salem, MA", "Exploring Salem, MA - October 2022", "Christmas in Salem"],
    "overview": "Exploring Salem, MA's historic sights and famous haunts.",
    "locale": "Salem", 
    "territory": "Massachusetts", 
    "country": "USA", 
    "places": [["ChIJo15HrGUU44kREi4broJXhBE", "Group tours available."], ["ChIJ9_27aW8U44kRA2HY1Vk_xxQ", "No more than 4 people per group."], ["ChIJI_iVlmQU44kRdKHvNkSVJd0", "Dogs OK on patio."], ["ChIJYza_FmgU44kRoW-cra6Ow0Y", "Reservations required."], ["ChIJaxSbrXsU44kRlkuQDQIsixM", "Costumes welcome."]]
    },
    {"name": ["Sleepless in Seattle", "5 Days in Seattle - May 2024", "Bachelorette Trip to Seattle, WA", "Seattle Summer Vacation", "Seattle Trip for Two", "John & Jane's Wedding in Seattle, WA", "Seattle Food Tour", "Seattle for the Winter Holidays", "Three-Days in Seattle, Washington", "Seattle, Washington - June 2022"], 
    "overview": "A trip to Seattle filled with delish eats, fun hikes, and lots of coffee.",
    "locale": "Seattle", 
    "territory": "Washington", 
    "country": "USA", 
    "places": [["ChIJSxh5JbJqkFQRxI1KoO7oZHs", "No photos allowed."], ["ChIJk63I_rNqkFQR3EtxoHQwzBM", "Masks required if dining indoors."], ["ChIJUX-M-a1qkFQRxtrx3nOQIKU", "Best view in Seattle."], ["ChIJ6x3yk7pqkFQRW2zXQJUlScA", "Check out the mini model of Seattle."], ["ChIJPQG7WLJqkFQRUXVHLnb3Lro", "Bring back a mug as a souvenir."]]
    },
    {"name": ["Sweet Home Chicago for the Holidays", "Adventures in Chitown", "Dharani & Amar's July Wedding in Chicago", "December 2022 Trip to Chicago for Swetha's and Amol's Wedding", "An L-evated Trip to downtown Chicago", "Whatchu talkin' about Willis Tower? June 2023 Trip to Chicago", "Chicago Stole a Pizza My Heart - Summer Trip to Chicago", "Relish the Good Times in Chicago November Trip", "CHICAGO! One Week in the Windy City", "Windy City Adventure"],
    "overview": "Three days and two nights.",
    "locale": "Chicago", 
    "territory": "Illinois", 
    "country": "USA", 
    "places": [["ChIJh479BaAsDogRWa7hmywCQCQ", "Great spot for photos, view of the Sears Tower, and close to Lake Michigan."], ["ChIJA5xPiqYsDogRBBCptdwsGEQ", "Mandatory trip to The Bean. Also a quick walk to the Art Institute."], ["ChIJX-RTBqksDogRRh_Q4ynbf_8", "Gorgeous views and lots of places to eat or grab a drink."], ["ChIJMViM4dssDogRdmIJH2z_Q10", "Fresh pasta."], ["ChIJk6QQWKUsDogR1vrLD_bdAEc", "Wicked! The Musical. Arrive 30 min before show starts."], ["ChIJKXA7AlXTD4gRsvBFJ8wG9x4", "Check out Nick Cave's Forothermore exhibit."]]
    },
    {"name": ["We'll Always Have Paris 2025", "2022 Anniversary in the City of Lights", "Christmas 2026 in Paris", "Family Reunion in Paris, France", "Paris Holds the Key to My Heart - September 2023 Vacation", "Eiffel in love with Paris Trip - March 2024", "Summer Vacation in Paris, France", "October in Paris", "Three Weeks in Paris - April 2023", "Paris Get-Away 2023"], 
    "overview": "Two romantic weeks enjoying Paris, France.",
    "locale": "Paris", 
    "territory": "France", 
    "country": "FRA", 
    "places": [["ChIJBxU8T_1t5kcRerSFrur9xN0", "Try the almond croissant."], ["ChIJA_6oQP5x5kcRNYQqafp0VQ4", "No children allowed."], ["ChIJe2jeNttx5kcRi_mJsGHdkQc", "Bring sunglasses."], ["ChIJATr1n-Fx5kcRjQb6q6cdQDY", "Free admission but tickets required to enter tower and the crypt."], ["ChIJD3uTd9hx5kcR1IQvGfr8dbk", "Reviews recommend at least 4 hours minimum visit to enjoy the museum. Break-up into multiple days, if possible."]]
    },
    {"name": ["Five Days in the Five Boroughs", "I Heart NYC 2023", "A Family Reunion Trip in New York 2024", "One Week in the Big Apple", "East Coast Tour - New York Leg", "Christmas & New Year Trip to New York", "Three-Day Weekend in NYC", "New York Birthday Trip", "New York for the Holidays", "Christmas at Rockefeller NYC"], 
    "overview": "New York sights and sounds.",
    "locale": "New York", 
    "territory": "New York", 
    "country": "USA", 
    "places": [["ChIJhWjFglZYwokR755nbhxKDlo", "Order the maitake wings."], ["ChIJ5bQPhMdZwokRkTwKhVxhP1g", "Gardens, architecture, and sweeping views of the city."], ["ChIJv-QVW6NZwokRFtWrN4mnkWM", "Best thin-crust in the world."], ["ChIJKxDbe_lYwokRVf__s8CPn-o", "Matisse: The Red Studio exhibit thru Sept 10."], ["ChIJqwvF8CZawokRwi6ijQhRGD0", "Get there before 10am or be prepared to wait a very long time."]]
    },
    {"name": ["Care for a Spot of Tea? England 2023", " A Summer Vacation Across the Pond", "Backpacking through England", "April Trip to London, England", "Exploring England - August Trip", "Birthday Trip to England", "Spring Holiday in England", "Anniversary Trip in England", "England Trip - October 2022", "Visiting the Lams in England 2024"], 
    "overview": "Two weeks exploring the past, present, and future history of England.",
    "locale": "London", 
    "territory": "England", 
    "country": "GBR", 
    "places": [["ChIJ40_ZncwEdkgRKYHPtm7wi28", "Try the Masala Negroni."], ["ChIJs4GOh8sEdkgRRiBFZKMP8ZE", "Bring comfortable walking shoes."], ["ChIJRXCcCSsbdkgR6VwJaM39_3I", "Local favorite for a spot of tea."], ["ChIJ68vBCFUbdkgR5CUqlcHifUA", "Free admission."], ["ChIJRUfpVQaRj4ARtHDUaCoX3j0", "Famous spot for fish & chips."]]
    },
    {"name": ["San Diego Weekend Get Away", "San Diego Trip - June 2022", "Holidaying in San Diego", "San Diego Visit 2023", "Coronado & San Diego - September 2023", "Susan's Birthday in San Diego", "Summer Vacation in San Diego", "San Diego Surfs & Eats", "A San Diego Wedding", "San Diego Wedding Shower"], 
    "overview": "Riding waves and soaking in a lot of sun.",
    "locale": "San Diego", 
    "territory": "California", 
    "country": "USA", 
    "places": [["ChIJd4ENW7JU2YARRg66LgvFYU8", "Copious plant-based options."], ["ChIJE-zr8z2q3oARY16lzCPo3Gk", "Pack a frisbee."], ["ChIJ_yXB3VlT2YARHJN8S2jhxso", "."], ["ChIJ68vBCFUbdkgR5CUqlcHifUA", "Rated San Diego's Best Authentic Mexican & Vegan Cuisine."], ["ChIJ0SGGW1dT2YAROOUV5ZU8Mc0", "Coffee and cats. Need I say meow-r?"]]
    }
]

# Create users to seed the database 
users_db = []

for first_name in first_names:
    fname = first_name
    lname = fake.unique.last_name()
    domain = fake.free_email_domain()
    email = f'{fname}.{lname}@{domain}'
    password = Bcrypt().generate_password_hash('wanderlust').decode('utf-8')
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

for user in users_id:

    for n in range(10):

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


# Create a few travel itineraries for each user
itineraries_db = []

start = datetime.now()
end = datetime.utcnow()

i = 0

for user in users_id:

    for itinerary in itinerary_choices:

        new_itinerary = model.Itinerary.create_itinerary(user_id=user, itinerary_name=itinerary["name"][i], overview=itinerary["overview"])
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
    
    i += 1


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