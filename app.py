from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, User, Donation


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})  # Adjust the origin as needed
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)
db.init_app(app)

# Create tables based on the defined models
with app.app_context():
    db.create_all()

@app.route('/donate', methods=['POST'])
def create_donation():
    data = request.get_json()  # Get data sent in JSON format

    # Create or update the user
    if data.get('anonymous'):
        user = User(anonymous=True)
    else:
        user = User(
            first_name=data.get('firstName'),
            last_name=data.get('lastName'),
            email=data.get('email'),
            country=data.get('country'),
            county=data.get('county'),
            phone=data.get('phone'),
            address=data.get('address'),
            company=data.get('company'),
            anonymous=data.get('anonymous', False)
        )
    
    db.session.add(user)
    db.session.commit()  # Commit to assign an ID

    # Create the donation linked to the user
    donation = Donation(
        user_id=user.id,
        amount=data['amount'],
        processing_fee=data['processingFee'] if data.get("includeProcessingFee", False) else 0,  # Corrected to use `None` and direct boolean check
        support_option=data['supportOption'],  
        donation_type='monthly' if data.get('frequency') == 'monthly' else 'one-time',
        pledge_date=int(data['pledgeDay']) if 'pledgeDay' in data and data['pledgeDay'] else None,
        dedication_name=data.get('dedicationName', None)  # Dedication name is optional
    )

    
    db.session.add(donation)
    db.session.commit()

    return jsonify({
        'message': 'Donation recorded successfully',
        'user_id': user.id,
        'donation_id': donation.id
    }), 201

# To run the application
if __name__ == "__main__":
    app.run(debug=True, port=5555)

