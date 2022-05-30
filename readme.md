# **Wanderlust**
A Hackbright Academy Capstone Project by [Luna Lam](https://github.com/lunaxlam)

## **Table of Contents**
* [Background](https://github.com/lunaxlam/wanderlust#background)
* [Tech Stack](https://github.com/lunaxlam/wanderlust#tech-stack) 
* [Features](https://github.com/lunaxlam/wanderlust#features)
* [Installation](https://github.com/lunaxlam/wanderlust#installation)


## **Background**
As avid travelers, my friends and I strive to make the most out of our adventures by developing day-by-day travel itineraries that detail lodging and dining accommodations, as well as places to see and explore. After our trips, we often pass along these thoughtfully-curated and personally-vetted itineraries to other friends and family as a guiding resource to enrich their own travels. 

While cloud storage platforms like [Google Drive](https://drive.google.com/) or [Dropbox](https://www.dropbox.com/) are useful for uploading and sharing the travel itineraries, which are often formatted through spreadsheet-programs such as [Microsoft Excel](https://www.microsoft.com/en-us/microsoft-365/excel), there is currently not a platform that provides a standard template design for a travel itinerary (which would help to improve readability for end-users) and publicly share the travel itinerary resource with a community of fellow travel enthusiasts. 

*Wanderlust* is a community-driven travel planning application that allows users to create, share, and clone personally curated travel itineraries through a standard form template. Users are able to filter travel itineraries by locale (city), territory (state), or country destinations.

The application utilizes the Google Maps JavaScript and Places APIs to auto-populate metadata about places, including name, address, location, website, ratings, and more. 

User passwords are hashed and salted with bcrypt.

## **Tech Stack**
Backend: Flask, Python, PostgreSQL, SQLAlchemy ORM<br />
Frontend: CSS 3, HTML5, JavaScript, Jinja, ReactJS<br/> 
APIs: Google Maps Platform - [Maps JavaScript API](https://developers.google.com/maps/documentation/javascript/), [Geocoding API](https://developers.google.com/maps/documentation/geocoding/overview), [Places API](https://developers.google.com/maps/documentation/places/web-service)<br />
Libraries: [Faker](https://faker.readthedocs.io/en/master/), [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/en/1.0.1/)

## **Features**
### [Section]
Detail <br />

### [Section]
Detail <br />

### [Section]
Detail <br /> 

### [Section]
Detail <br /> 

## **Installation**
To run *Wanderlust*: <br />

Clone or fork the [repository](https://github.com/lunaxlam/wanderlust):

```
https://github.com/lunaxlam/wanderlust
```

In the project directory, create and activate a virtual environment:
```
virtualenv env
source env/bin/activate
```

Install the project dependencies:
```
pip3 install -r requirements.txt
```

Create and save your Flask and [Google API](https://developers.google.com/maps/get-started) secret keys in a file called <kbd>secrets.sh</kbd> in the following format:
```
export FLASK_SECRET_KEY="YOUR_KEY_HERE"
export GOOGLE_API_KEY="YOUR_KEY_HERE"
```

Source your secret keys:
```
source secrets.sh
```

Seed the database:
```
python3 seed.py
```

Run the application:
```
python3 server.py
```

In your web browser, navigate to:
```
localhost:5000/
```
You can now access *Wanderlust* ! Happy travels.
