"""CRUD operations for creating data."""

from model import db, connect_to_db, User, Follower, Itinerary, Item


def create_user(email, password, username, fname, lname, locale, territory, country, about_me):
    """Create and return a new user"""

    user = User(email=email, 
                password=password, 
                username=username, 
                fname=fname, 
                lname=lname, 
                locale=locale, 
                territory=territory, 
                country=country, 
                about_me=about_me)
    
    return user


def get_users():
    """Return all users"""

    return db.session.query(User)


def get_user_by_id(user_id):
    """Return a user by user_id"""

    return User.query.get(user_id)


def get_user_by_username(username):
    """Return a user by username"""

    return User.query.get(username)


def create_follower(follower_id, user_followed_id):
    """Create and return a follower"""

    follower = Follower(follower_id=follower_id,
                        user_followed_id=user_followed_id)
    
    return follower


def get_followers():
    """Return all followers"""

    return db.session.query(Follower)


def get_followers_by_user_followed_id(user_followed_id):
    """Return all followers of a followed-user"""

    pass


def get_following_by_follower_id(follower_id):
    """Return all following by a follower-user"""

    pass


def create_itinerary(user_id, itinerary_name, overview):

    itinerary = Itinerary(user_id=user_id,
                            itinerary_name=itinerary_name,
                            overview=overview)
    
    return itinerary


def get_itinerary_by_user_id(user_id):
    pass


def create_item(itinerary_id, item_name, date, start_time, end_time, name_or_description,
                address, locale, territory, country, place_id):
    
    item = Item(itinerary_id=itinerary_id,
                item_name=item_name,
                date=date,
                start_time=start_time,
                end_time=end_time,
                name_or_description=name_or_description,
                address=address,
                locale=locale,
                territory=territory,
                country=country,
                place_id=place_id)
    
    return item


if __name__ == "__main__":
    from server import app
    
    connect_to_db(app)