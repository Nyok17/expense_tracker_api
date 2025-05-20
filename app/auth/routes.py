from flask import Blueprint, jsonify, request
from app.extensions import db, bcrypt
from flask_jwt_extended import create_access_token
from app.models import User
from .schemas import RegisterSchema, LoginSchema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth', __name__)
register_schema = RegisterSchema()
login_schema = LoginSchema()


@auth_bp.route('/')
def home():
    """A function to display the default route"""
    return "Hello world!"

@auth_bp.route('/register', methods=['POST'])
def register_users():
    """A function to register users"""
    try:
        data = register_schema.load(request.get_json())
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = User(username=data['username'], email=data['email'], password=hashed_password)

        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            "status": "success",
            "message": "User registered successfully",
        }), 201
    
    except ValidationError as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 400
    
    except IntegrityError as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "error": str(e)
        })


@auth_bp.route('/login', methods=['POST'])
def login_users():
    """A function to login users"""
    try:
        data = login_schema.load(request.get_json())
        user = User.query.filter_by(email=data['email']).first()
        if not user or not bcrypt.check_password_hash(user.password, data['password']):
            raise ValidationError("Wrong email or password")
        db.session.commit()

        access_token = create_access_token(identity=str(user.id))

        return jsonify({
            "status": "success",
            "access_token": access_token,
            "message": "User logged in successfully"
        }), 200
    
    except ValidationError as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 400
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500