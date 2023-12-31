from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(50))
    user_profile = db.relationship('Profile')
    user_quote = db.relationship('Quote')

    def __repr__(self):
        return f"User('{self.first_name}')"

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50))
    address1 = db.Column(db.String(100))
    address2 = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(9))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Profile('{self.full_name}')"
    
class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100))
    delivery_address = db.Column(db.String(100))
    gallons_requested = db.Column(db.String(100))
    suggest_price = db.Column(db.String(10))
    total_price = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Quote('{self.delivery_address}')"
