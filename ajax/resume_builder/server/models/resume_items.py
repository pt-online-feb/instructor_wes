from sqlalchemy.sql import func
from config import db

class ResumeItem(db.Model):
    __tablename__ = 'resume_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    content_type = db.Column(db.String(45), nullable=False)
    name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_year = db.Column(db.Integer, nullable=False)
    end_year = db.Column(db.Integer, nullable=False)
    created_at = db.Column(
        db.DateTime,
        server_default=func.now()
    )
    updated_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )
    user=db.relationship(
        'User',
        foreign_keys=[user_id],
        backref=db.backref(
            "resume_items",
            cascade="all, delete-orphan"
        )
    )

    @classmethod
    def validate(cls, form):
        print(form)
        errors = []
        CONTENT_TYPES = ["PROJECT", "JOB", "EDUCATION"]
        if form['content_type'] not in CONTENT_TYPES:
            errors.append("Content type invalid.")

        if len(form['name']) < 1:
            errors.append("Must include name.")
        
        if len(form['description']) < 10:
            errors.append("Description must be at least 10 characters long.")

        try:
            start_year = int(form['start_year'])
            if start_year < 1000:
                print("year not 4 digits")
                raise Exception("year not 4 digits")
        except:
            errors.append("Start year must be a valid 4 digit integer.")

        try:
            end_year = int(form['end_year'])
            if end_year < 1000:
                print("year not 4 digits")
                raise Exception("year not 4 digits")
        except:
            errors.append("Start year must be a valid 4 digit integer.")

        return errors

    @classmethod
    def create(cls, form, user_id):
        resume_item = cls(
            content_type=form['content_type'],
            name=form['name'],
            description=form['description'],
            start_year=int(form['start_year']),
            end_year=int(form['end_year']),
            user_id=user_id
        )
        db.session.add(resume_item)
        db.session.commit()
