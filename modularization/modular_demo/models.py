from sqlalchemy.sql import func
from config import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    @classmethod
    def validate(cls, form_info):
        errors = []
        if len(form_info['first_name']) < 2:
            errors.append("First name must be at least 2 characters long")
        if len(form_info['last_name']) < 2:
            errors.append("Last name must be at least 2 characters long")
        return errors

    @classmethod
    def create(cls, form):
        user = User(
            first_name=form['first_name'],
            last_name=form['last_name'],
            email=form['email']
        )
        db.session.add(user)
        db.session.commit()