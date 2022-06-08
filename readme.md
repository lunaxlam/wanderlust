# **Wanderlust**
A Hackbright Academy Capstone Project by [Luna Lam](https://github.com/lunaxlam)

## **Table of Contents**
* [Background](https://github.com/lunaxlam/wanderlust#background)
* [Tech Stack](https://github.com/lunaxlam/wanderlust#tech-stack) 
* [Features](https://github.com/lunaxlam/wanderlust#features)
* [Installation](https://github.com/lunaxlam/wanderlust#installation)
* [Version 2.0](https://github.com/lunaxlam/wanderlust#)


## **Background**
As avid travelers, my friends and I strive to make the most out of our adventures by developing day-by-day travel itineraries that detail lodging and dining accommodations, as well as places to see and explore. After our trips, we often pass along these thoughtfully-curated and personally-vetted itineraries to other friends and family as a guiding resource to enrich their own travels. 

While cloud storage platforms like [Google Drive](https://drive.google.com/) or [Dropbox](https://www.dropbox.com/) are useful for uploading and sharing the travel itineraries, which are often formatted through spreadsheet-programs such as [Microsoft Excel](https://www.microsoft.com/en-us/microsoft-365/excel), there is currently not a platform that provides a standard template design for a travel itinerary (which would help to improve readability for end-users) and publicly share the travel itinerary resource with a community of fellow travel enthusiasts. 

### Wanderlust
*Wanderlust* is a full-stack travel planning application that allows users to create, share, and clone personally curated travel itineraries through a standard form template. Users are able to filter travel itineraries by locale (city), territory (state), or country destinations.

The application utilizes the Google Maps JavaScript and Places APIs to auto-populate metadata about places, including name, address, location, website, ratings, and more. 

User passwords are hashed and salted with bcrypt.

## **Tech Stack**
Backend: Flask, Python, PostgreSQL, SQLAlchemy ORM<br />
Frontend: CSS 3, HTML5, JavaScript, Jinja, ReactJS<br/> 
APIs: Google Maps Platform - [Maps JavaScript API](https://developers.google.com/maps/documentation/javascript/), [Geocoding API](https://developers.google.com/maps/documentation/geocoding/overview), [Places API](https://developers.google.com/maps/documentation/places/web-service); [Random User Generator](https://randomuser.me/)<br />
Libraries: [Faker](https://faker.readthedocs.io/en/master/), [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/en/1.0.1/)

## **Features**
### Login and New Account Registration
Returning users are able to login by authenticating their email and password in the login form embedded in the navigation bar.

<img src="/static/images/sitenav/home.gif">

New users are able to register an account by clicking on the "Create Account" link.

<img src="/static/images/sitenav/createaccount.png">

### Edit Account, View Follower/Following Activity, and View User Profile
After logging in, users are routed to their profile where they can:
- Edit their account information
- View their "Followers" and "Following" activity

<img src="/static/images/sitenav/profile.png">

Users are also able to view their personalized travel map with pinned markers of previously-visited destinations, and view their past travel itineraries 

<img src="/static/images/sitenav/usermapitin.png">

### Create New Itinerary
Users are able to create a new travel itinerary.

<img src="/static/images/sitenav/createitinerary.png">

### View, Edit, and Delete a Saved Itinerary
Users are able to view and delete a saved itinerary, as well as add additional destinations to a saved itinerary.

<img src="/static/images/sitenav/itinerary.png">

### View, Edit, and Delete Saved Activities
Users are able to view, edit, and delete saved itinerary activities. Place-related metadata for each saved activity are rendered in real-time by an API call to the Google Places API. 

<img src="/static/images/sitenav/editactivity.png">

### Search New Activity Location
Users are able to search for a new activity location by conducting an autocomplete location search by name or address. Alternatively, users are able to search for a new activity location by point of interest, which makes a regular HTTP GET request to the Google Places Text Search API endpoint. 

<img src="/static/images/sitenav/addactivity.png">

### View Location Search Results
Users are able to view up to 20 location search results per page. 

<img src="/static/images/sitenav/searchresults.png">

Users are also able to click on the "View More Results" button to return additional results. 

<img src="/static/images/sitenav/viewmore.png">

### View Place Metadata and Save Location to a New Activity
Users are able to view a specific location and view place-related metadata such as ratings, website, address, phone number, and more. Users are then able to save the location to a new activity card.

<img src="/static/images/sitenav/place.png">

### View and Filter Other User Itineraries
Users are able to view itineraries of other users and filter itineraries by locale (city), territory (state), and country.

<img src="/static/images/sitenav/filter.png">

### View Other Users
Users are able to view all users of the application. 

<img src="/static/images/sitenav/community.png">

### View Another User's Profile and Follow Users
Users are able to view another user's profile and follow another user.

<img src="/static/images/sitenav/anotheruser.png">


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

## **Version 2.0**
* Enable users to upload a custom profile picture
* Add Google OAuth to handle credential management and authentication
* Display sorted itinerary activities by activity date
