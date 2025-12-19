# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Task 3: Get earthquake by ID
@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    quake = Earthquake.query.filter_by(id=id).first()
    if quake:
        return jsonify(quake.to_dict()), 200
    return jsonify({"message": f"Earthquake {id} not found."}), 404

# Task 4: Get earthquakes by minimum magnitude
@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    return jsonify({
        "count": len(quakes),
        "quakes": [q.to_dict() for q in quakes]
    }), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)