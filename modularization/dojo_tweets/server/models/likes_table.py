from sqlalchemy.sql import func
from config import db

likes_table=db.Table('likes',
    db.Column(
        'tweet_id',
        db.Integer,db.ForeignKey(
            'tweets.id',
            ondelete="cascade"
        ),
        primary_key=True
    ),
    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    ),
    db.Column(
        'created_at',
        db.DateTime,
        server_default=func.now()
    )
)