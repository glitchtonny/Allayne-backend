#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, jsonify
from flask_restful import Resource
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity



# Local imports
from config import app, db, api
# Add your model imports
from models import User


bcrypt=Bcrypt(app)


# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

@app.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Invalid data provided'}), 400
    
    hashed_password= bcrypt.generate_password_harsh(data['password'])
    new_user = User(
        username=data['username'],
        password=hashed_password,
        email=data.get('email'),
        role=data.get('role')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Invalid data provided'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'id': user.id, 'role': user.role})
        return jsonify({
            'access_token': access_token,
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }), 200
    return jsonify({'message': 'Invalid credentials'}), 401

    



if __name__ == '__main__':
    app.run(port=5555, debug=True)
