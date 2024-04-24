from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    county = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    company = db.Column(db.String(100), nullable=True)
    anonymous = db.Column(db.Boolean, default=False)

    donations = db.relationship('Donation', backref='user', lazy=True)

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    processing_fee = db.Column(db.Float, nullable=False)
    support_option = db.Column(db.String(100), nullable=False)
    donation_type = db.Column(db.String(50), nullable=False)  # 'one-time', 'monthly'
    pledge_date = db.Column(db.Integer, nullable=True)  # Day of the month for monthly donations
    dedication_name = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Donation {self.id} from User {self.user_id}>"
