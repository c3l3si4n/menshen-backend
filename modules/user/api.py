from flask import Blueprint, request, abort, jsonify
from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker
from argon2 import PasswordHasher

from .model import User
import json
engine = create_engine(
    'postgresql://postgres@localhost:5432/menshen', echo=True)

users_bp = Blueprint('users', __name__)
@users_bp.route('/api/users/register', methods=['POST'])
def register():
    ds = request.json
    response = {}
    if not 'name' in ds:
        response["message"] = "name field missing."
        return jsonify(response), 400
    if not 'email' in ds:
        response["message"] = "email field missing."
        return jsonify(response), 400

    if not 'password' in ds:
        response["message"] = "password field missing."
        return jsonify(response), 400

    inputName = ds['name']
    inputEmail = ds['email']

    ph = PasswordHasher()

    inputPassword = ph.hash(ds['password'])

    Session = sessionmaker(bind=engine)
    session = Session()
    ret = session.query(exists().where(User.email == inputEmail)).scalar()
    session.commit()

    if ret:  # check if email exists
        response["message"] = "email already is registered."
        return jsonify(response), 400

    user = User(email=inputEmail, full_name=inputName, password=inputPassword)

    session.add(user)
    session.commit()
    session.close()
    return '', 201
