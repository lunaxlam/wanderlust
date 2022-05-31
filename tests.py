"""Tests for Wanderlust Flask app"""

import unittest
import server
import test_data


class WanderlustTests(unittest.TestCase):
    """Tests for Wanderlust app"""

    def setUp(self):
        """Run before every test"""
        
        server.app.config['TESTING'] = True
        server.app.config[server.app.secret_key] = 'key'
        self.client = server.app.test_client()

        with self.client as c:
            with c.session_transaction() as session:
                session["user_id"] = 1

        test_data.connect_db()
        test_data.example_data()
    
    def tearDown(self):
        """Run at the end of every test"""

        test_data.drop_db()
    
    def test_homepage(self):
        """Check if homepage successfully renders"""

        result = self.client.get("/")
        self.assertIn(b"<h1>Welcome to Wanderlust!</h1>", result.data)

    def test_login_valid_user(self):
        """Check if logged-in users see the right view"""

        login_info = {"email": "ellie.wang@gmail.com", "password": "ewang"}

        result = self.client.post("/login", data=login_info, follow_redirects=True)

        self.assertIn(b"<h2>My Adventure Map</h2>", result.data)
    
    def test_login_wrong_pw(self):
        """Check if user is redirected to homepage if password is incorrectly entered"""

        login_info = {"email": "ellie.wang@gmail.com", "password": "alam"}

        result = self.client.post("/login", data=login_info, follow_redirects=True)

        self.assertNotIn(b"<h2>My Adventure Map</h2>", result.data)
        self.assertIn(b"<h1>Welcome to Wanderlust!</h1>", result.data)
    
    def test_login_no_username(self):
        """Check if user is directed to homepage if user does not exist in database"""

        login_info = {"email": "earl.grey@yahoo.com", "password": "egrey"}

        result = self.client.post("/login", data=login_info, follow_redirects=True)

        self.assertNotIn(b"<h2>My Adventure Map</h2>", result.data)
        self.assertIn(b"<h1>Welcome to Wanderlust!</h1>", result.data)

    def test_existing_user(self):
        """Check if user is directed to the user's userpage if already in database"""

        user_info = {"email": "ellie.wang@gmail.com", 
                    "password": "ewang",
                    "username": "ewang",
                    "fname": "Ellie",
                    "lname": "Wang",
                    "locale": "Seattle",
                    "territory": "Washington",
                    "country": "USA",
                    "about_me": "Culinary Genius \U0001F9C1 Coffee Fiend \U00002615 doggo parent \U0001F429"
                    }

        result = self.client.post("/create_user", data=user_info, follow_redirects=True)

        self.assertNotIn(b"<h2>My Adventure Map</h2>", result.data)
        self.assertIn(b"<h1>Welcome to Wanderlust!</h1>", result.data)
    
    def test_create_user(self):
        """Check if newly created user is directed to the user's userpage if after account creation"""

        user_info = {"email": "earl.grey@gmail.com", 
                    "password": "egrey",
                    "username": "egrey",
                    "fname": "Earl",
                    "lname": "Grey",
                    "locale": "Birmingham",
                    "territory": "England",
                    "country": "GBR",
                    "about_me": "Tea connoiseur."
                    }

        result = self.client.post("/create_user", data=user_info, follow_redirects=True)

        self.assertNotIn(b"<h2>My Adventure Map</h2>", result.data)
        self.assertIn(b"<h2>My Itineraries</h2>", result.data)
        self.assertNotIn(b"<h1>Welcome to Wanderlust!</h1>", result.data)
  
    def test_all_users(self):
        """Check if all users page successfully renders"""

        result = self.client.get("/users")

        self.assertIn(b"<h1>Wanderlust Community</h1>", result.data)
    
    def test_user_profile(self):
        """Check if user profile page successfully renders"""

        with self.client as c:
            with c.session_transaction() as session:
                session["user"] = "ewang"
                session["username"] = "ewang" 

        result = self.client.get(f"/user/{session['username']}")
        self.assertIn(b"<h2>My Adventure Map</h2>", result.data)

    def test_follow_me(self):
        """Check if a user is successfully saved to a log-in user's page"""

        with self.client as c:
            with c.session_transaction() as session:
                session["user"] = "andrewlam"
                session["user_id"] = 1
                session["username"] = "andrewlam" 

        result = self.client.get(f"/user/{session['username']}/follow_me", follow_redirects=True)
        self.assertIn(b"<h2>My Itineraries</h2>", result.data)

    def test_create_itinerary(self):
        """Check if a user is successfully saved to a log-in user's page"""

        with self.client as c:
            with c.session_transaction() as session:
                session["user_id"] = 1
        
        itinerary_info = {
            "name": "A Byte of the Big Apple",
            "overview": "8 Days in NYC",
            "locale": "New York",
            "territory": "New York",
            "country": "USA"
        }

        result = self.client.post(f"/create_itinerary", data=itinerary_info, follow_redirects=True)
        self.assertIn(b"<h2>Search Location to Add Activity</h2>", result.data)

    def test_all_itineraries(self):
        """Check if all itinerary page successfully renders"""

        result = self.client.get("/itineraries")
        self.assertIn(b"<h1>Wanderlust Itineraries</h1>", result.data)
        self.assertIn(b"<h2>Filter:</h2>", result.data)

    def test_view_itinerary(self):
        """Check if an individual itinerary page successfully renders"""

        with self.client as c:
            with c.session_transaction() as session:
                session["itinerary_id"] = 1

        result = self.client.get(f"/itinerary/{session['itinerary_id']}")
        self.assertIn(b"<h2>Activities</h2>", result.data)
    
    def test_clone_itinerary(self):
        """Check if cloning an itinerary is successful"""

        with self.client as c:
            with c.session_transaction() as session:
                session["itinerary_id"] = 1
                session["user_id"] = 1
        
        itinerary_info = {
            "name": "A Byte of the Big Apple",
            "overview": "8 Days in NYC"
        }

        result = self.client.post(f"/itinerary/{session['itinerary_id']}", data=itinerary_info, follow_redirects=True)
        self.assertIn(b"<h2>Search Location to Add Activity</h2>", result.data)

    def test_add_destination(self):
        """Check if add_destiination successfully renders"""

        with self.client as c:
            with c.session_transaction() as session:
                session["itinerary_id"] = 1
        
        destination_info = {
            "locale": "Denver",
            "territory": "Colorado",
            "country": "USA"
        }

        result = self.client.post(f"/itinerary/{session['itinerary_id']}/add_destination", data=destination_info, follow_redirects=True)
        self.assertIn(b"<h2>Search Location to Add Activity</h2>", result.data)

    def test_all_users(self):
        """Check if all users page successfully renders"""

        result = self.client.get("/users")
        self.assertIn(b"<h1>Wanderlust Community</h1>", result.data)

    def test_countries(self):
        """Check if countries page successfully renders"""

        result = self.client.get("/countries")
        self.assertIn(b"<h1>Wanderlust Countries</h1>", result.data)
        self.assertIn(b"<h2> Country Code | Country</h2>", result.data)

    def test_logout(self):
        """Check if homepage successfully renders when a user logs-out"""

        with self.client as c:
            with c.session_transaction() as session:
                session["user"] = "ewang"

        result = self.client.get("/logout", follow_redirects=True)
        self.assertIn(b"<h1>Welcome to Wanderlust!</h1>", result.data)
    

if __name__ == "__main__":
    unittest.main()