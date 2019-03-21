from sqlalchemy.sql import func
from config import db
from server.models.likes_table import likes_table

class Tweet(db.Model):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    content = db.Column(db.String(255), nullable=False)
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
            "tweets",
            cascade="all, delete-orphan"
        )
    )
    liked_by=db.relationship(
        'User',
        secondary=likes_table,
        backref="liked_tweets"
    )

    @classmethod
    def validate(cls, form):
        errors = []
        if len(form['content']) > 255:
            errors.append("Tweet cannot exceed 255 characters in length.")
        if len(form['content']) < 1:
            errors.append("Tweet must not be left empty.")
        return errors

    @classmethod
    def create(cls, form, user_id):
        tweet = cls(
            content=form['content'],
            user_id=user_id
        )
        db.session.add(tweet)
        db.session.commit()

    @classmethod
    def get_tweets_from_users(cls, user_ids=None):
        if not user_ids:
            return cls.query.order_by(cls.created_at.desc()).all()
        
        return cls.query.filter(cls.user_id.in_(user_ids)).order_by(cls.created_at.desc()).all()
