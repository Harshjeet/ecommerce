from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import User, db, Role

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['POST'])
def create_user():
    """ User Signup with JWT Token """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    role_input = data.get('role')

    if not email or not password or not username or not role_input:
        return jsonify({"error": "Missing required fields"}), 400

    # Validate Role
    if role_input not in [role.value for role in Role]:
        return jsonify({"error": "Invalid role. Choose from 'admin', 'store_manager', or 'customer'"}), 400

    user_exists = User.query.filter_by(email=email).first()
    if user_exists:
        return jsonify({"error": "User already exists"}), 400

    user = User(
        email=email,
        username=username,
        password=password,  # Ensure password is hashed in User model
        role=Role(role_input)
    )

    db.session.add(user)
    db.session.commit()

    # Generate JWT Token
    access_token = create_access_token(identity={"email": user.email, "role": user.role.value})

    return jsonify({
        "message": "User created successfully",
        "user_id": user.id,
        "role": user.role.value,
        "token": access_token
    }), 201

@auth.route('/login', methods=['POST'])
def login_user():
    """ User Login with JWT Token """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Generate JWT Token
    access_token = create_access_token(identity={"email": user.email, "role": user.role.value})

    return jsonify({
        "message": "Login successful",
        "user_id": user.id,
        "role": user.role.value,
        "token": access_token
    }), 200
