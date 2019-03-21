from sqlalchemy.sql import func
from config import db

followers_table = db.Table('followers',
    db.Column(
        'follower_id',
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    ),
    db.Column(
        'followee_id',
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