from app.extensions import db
from app.models import Expense
from .schemas import ExpenseSchema
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import jwt_required, get_jwt_identity


expense_schema = ExpenseSchema()
expense_bp = Blueprint('expense', __name__)

@expense_bp.route('/expenses', methods=['POST'])
@jwt_required()
def add_expense():
    """A function to add and save expenses to the db"""
    try:
        data = expense_schema.load(request.get_json())
        user_id = int(get_jwt_identity())
        if not user_id:
            raise ValidationError("Missing or invalid token")
        new_expense = Expense(expense=data['expense'], amount=data['amount'], category=data['category'], user_id=user_id)
        db.session.add(new_expense)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Expense added successfully",
            "expense": expense_schema.dump(new_expense)
        }), 201
    
    except ValidationError as e:
        return jsonify({
            "status": "error",
            "error": e.messages
        }), 400
    
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500
    

@expense_bp.route('/expenses', methods=['GET'])
@jwt_required()
def get_expenses():
    """A function to retrieve all the expenses"""
    try:
        user_id = get_jwt_identity()
        filter_type = request.args.get('filter')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        query = Expense.query.filter_by(user_id=user_id)

        now = datetime.now(timezone.utc)

        if filter_type == 'week':
            query = query.filter(Expense.created_at >= now - timedelta(weeks=1))
        elif filter_type == 'month':
            query = query.filter(Expense.created_at >= now - timedelta(days=30))
        elif filter_type == '3months':
            query = query.filter(Expense.created_at >= now - timedelta(days=90)) 
        elif start_date and end_date:
            try:
                start = datetime.fromisoformat(start_date).replace(tzinfo=timezone.utc)
                end = datetime.fromisoformat(end_date).replace(tzinfo=timezone.utc)
                query = query.filter(Expense.created_at.between(start, end))
            except ValueError:
                return jsonify({
                    "status": "error",
                    "error": "Invalid date format"
                })
            
        expenses = query.order_by(Expense.created_at.desc()).all()
        
        return jsonify({
            "status": "success",
            "expenses": expense_schema.dump(expenses, many=True)
        }), 200
    
    except ValidationError as e:
        return jsonify({
            "status": "error",
            "error": e.messages
        }), 400
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@expense_bp.route('/expenses/<int:id>', methods=['GET'])
@jwt_required()
def get_expense(id):
    """A function to get a single expense"""
    try:
        user_id = get_jwt_identity()
        expense = Expense.query.filter_by(user_id=user_id, id=id).first_or_404()
        return jsonify({
            "status": "success",
            "expense": expense_schema.dump(expense)
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500
    

@expense_bp.route('/expenses/<int:id>', methods=['PUT'])
@jwt_required()
def update_expenses(id):
    """A function to update expenses"""
    try:
        user_id = get_jwt_identity()
        data = expense_schema.load(request.get_json(), partial=True)
        expense = Expense.query.filter_by(user_id=user_id, id=id).first_or_404()
        if 'expense' in data:
            expense.expense = data['expense']
        if 'amount' in data:
            expense.amount = data['amount']
        if 'category' in data:
            expense.category = data['category']

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Expense updated successfully"
        }), 200
    
    except ValidationError as e:
        return jsonify({
            "status": "error",
            "error": e.messages
        }), 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500
    
@expense_bp.route('/expenses/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_expenses(id):
    try:
        user_id = get_jwt_identity()
        expense = Expense.query.filter_by(user_id=user_id, id=id).first_or_404()
        db.session.delete(expense)
        db.session.commit()

        return jsonify({
        "status": "success",
        "message": "Expense deleted successfully"
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500