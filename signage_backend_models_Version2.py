from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    last_login = db.Column(db.DateTime)

class Asset(db.Model):
    __tablename__ = 'assets'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), unique=True, nullable=False)
    original_name = db.Column(db.String(255))
    type = db.Column(db.String(10)) # image|video|audio|web
    path = db.Column(db.String(512))
    url = db.Column(db.String(512))
    duration_sec = db.Column(db.Integer)
    volume = db.Column(db.Integer)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    codec = db.Column(db.String(32))
    size_bytes = db.Column(db.Integer)
    thumb_path = db.Column(db.String(255))
    status = db.Column(db.String(16), default="ready") # ready|transcoding|error
    created_at = db.Column(db.DateTime, default=func.now())

class Playlist(db.Model):
    __tablename__ = 'playlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    is_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

class PlaylistItem(db.Model):
    __tablename__ = 'playlist_items'
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'))
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'))
    position = db.Column(db.Integer)
    per_item_duration_sec = db.Column(db.Integer)
    per_item_volume = db.Column(db.Integer)

class Schedule(db.Model):
    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'))
    start_datetime = db.Column(db.DateTime)
    end_datetime = db.Column(db.DateTime)
    days_of_week = db.Column(db.Integer)  # bitmask
    priority = db.Column(db.Integer, default=1)
    enabled = db.Column(db.Boolean, default=True)

class Setting(db.Model):
    __tablename__ = 'settings'
    key = db.Column(db.String(64), primary_key=True)
    value = db.Column(db.Text) # JSON

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    ts = db.Column(db.DateTime, default=func.now())
    level = db.Column(db.String(16))
    source = db.Column(db.String(32))
    message = db.Column(db.String(255))
    extra = db.Column(db.Text) # JSON

def init_db():
    db.create_all()

def create_default_admin():
    from .auth import hash_password
    if not User.query.filter_by(username="admin").first():
        u = User(username="admin", password_hash=hash_password("change_me"))
        db.session.add(u)
        db.session.commit()