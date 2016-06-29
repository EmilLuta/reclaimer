from flask.ext.login import UserMixin

from app import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    picture_url = db.Column(db.String(128))
    social_id = db.Column(db.String(128), unique=True)
    social_profile_url = db.Column(db.String(128))

    def __init__(self, first_name, last_name, email, picture_url, social_id, social_profile_url):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.picture_url = picture_url
        self.social_id = social_id
        self.social_profile_url = social_profile_url

    def __repr__(self):
        return 'User #{} - {} {}'.format(self.id, self.first_name, self.last_name)

    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)


class LocationSeed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(128))
    city_name = db.Column(db.String(128))

class IATACode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10))
    name = db.Column(db.String(128))
    country_code = db.Column(db.String(10))

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.String(255))
    price = db.Column(db.Float)
    location_seed_id = db.Column(db.Integer, db.ForeignKey('location_seed.id'), nullable=False)
    location_seed = db.relationship('LocationSeed', backref=db.backref('flights', uselist=True, lazy='select'))

class HotDeal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'), nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'), nullable=False)
    location_data_id = db.Column(db.Integer, db.ForeignKey('location_data.id'), nullable=False)
    ranking = db.Column(db.Integer)

    hotel = db.relationship('Hotel', backref=db.backref('hot_deals', uselist=True, lazy='select'))
    flight = db.relationship('Flight', backref=db.backref('hot_deals', uselist=True, lazy='select'))
    location_data = db.relationship('LocationData', backref=db.backref('hot_deals', uselist=True, lazy='select'))

class SearchQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    query = db.Column(db.String(255))
    user = db.relationship('User', backref=db.backref('search_queries', uselist=True, lazy='select'))

class LocationData(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    location_seed_id = db.Column(db.Integer, db.ForeignKey('location_seed.id'), nullable=False)
    location_seed = db.relationship('LocationSeed', backref=db.backref('location_data', uselist=True, lazy='select'))

    restaurant_inexpensive_meal = db.Column(db.String(128))
    restaurant_decent_couple_meal = db.Column(db.String(128))
    local_beverage = db.Column(db.String(128))
    imported_beverage = db.Column(db.String(128))
    coffee = db.Column(db.String(128))
    soda = db.Column(db.String(128))
    water = db.Column(db.String(128))
    ticket_transport = db.Column(db.String(128))
    taxi_start = db.Column(db.String(128))
    taxi_km = db.Column(db.String(128))


class DestinationData(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    location_seed_id = db.Column(db.Integer, db.ForeignKey('location_seed.id'), nullable=False)
    location_seed = db.relationship('LocationSeed', backref=db.backref('destinations', uselist=True, lazy='select'))

    longitude = db.Column(db.String(128))
    latitude = db.Column(db.String(128))
    destination_id = db.Column(db.Integer)


class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    destination_data_id = db.Column(db.Integer, db.ForeignKey('destination_data.id'), nullable=False)
    destination_data = db.relationship('DestinationData', backref=db.backref('hotels', uselist=True, lazy='select'))

    price = db.Column(db.String(128))
    name = db.Column(db.String(128))
    address = db.Column(db.String(255))
    review = db.Column(db.Float)
    trip_advisor_review = db.Column(db.Float)
    # site_url = db.Column(db.String(255))

    @property
    def city(self):
        return self.destination_data.location_seed.city_name

    @property
    def country(self):
        return self.destination_data.location_seed.country_name
