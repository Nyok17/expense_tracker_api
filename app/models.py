from .extensions import db
from datetime import datetime, timezone


class User(db.Model):
    """A class to describe 'User' model with its attributes"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    expenses = db.relationship('Expense', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"
    
class Expense(db.Model):
    """A class to describe 'Expense' model with its attributes"""
    id = db.Column(db.Integer, primary_key=True)
    expense = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.Date, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.Date, 
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
        )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Expense {self.expense} {self.amount}>"
