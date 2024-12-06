from flask import Blueprint, request, jsonify
from app.models import User
from app import db
import bcrypt
import jwt
import datetime
from flask_cors import cross_origin

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/api/example', methods=['GET'])
def example():
    return "Hello world"

@auth_bp.route('/api/register', methods=['POST'])
@cross_origin
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    firebase_token = 'firebaseToken'

    if not username or not password or not firebase_token: return jsonify({"message": "Missing required fields"}), 400

    if User.query.filter_by(username=username).first(): return jsonify({"message": "User already exists"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = User(username=username, password=hashed_password.decode('utf-8'), firebase_token=firebase_token)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({"message": "Invalid username or password"}), 401

    token = jwt.encode({
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, "qazwsx12", algorithm="HS256")

    return jsonify({"message": "Login successful", "token": token}), 200


def decode_jwt(token):
    try:
        decoded = jwt.decode(token, "qazwsx12", algorithms=["HS256"])
        return decoded["user_id"]
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
