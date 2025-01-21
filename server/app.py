#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    # Query the Earthquake with the given ID
    earthquake = Earthquake.query.get(id)
    
    if earthquake:
        # If found, return earthquake attributes as JSON
        return jsonify({
            'id': earthquake.id,
            'magnitude': earthquake.magnitude,
            'location': earthquake.location,
            'year': earthquake.year
        })
    else:
        # If not found, return error message as JSON with the 'message' key
        return jsonify({'message': f'Earthquake {id} not found.'}), 404

@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    # Query for all earthquakes with magnitude >= the given value
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    # Prepare the response data
    earthquakes_data = [
        {
            'id': eq.id,
            'location': eq.location,
            'magnitude': eq.magnitude,
            'year': eq.year
        }
        for eq in earthquakes
    ]
    
    # Return the count and list of earthquakes
    return jsonify({
        'count': len(earthquakes_data),
        'quakes': earthquakes_data
    })



if __name__ == '__main__':
    app.run(port=5555, debug=True)
