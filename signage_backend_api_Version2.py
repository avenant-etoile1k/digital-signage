from flask import Blueprint, request, jsonify, render_template, redirect, url_for, send_from_directory, flash
from flask_login import login_required, login_user, logout_user, current_user
from .models import db, Asset, Playlist, PlaylistItem, Schedule, Event, Setting
from .auth import verify_password, hash_password
from .thumbnails import generate_thumbnail
from .transcode import enqueue_transcode
from .settings import load_config
import os

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route("/")
@login_required
def dashboard():
    return render_template("dashboard.html")

# --- Auth routes
@api_blueprint.route("/login", methods=["GET", "POST"])
def login():
    from .models import User
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and verify_password(user, password):
            login_user(user)
            user.last_login = db.func.now()
            db.session.commit()
            return redirect(url_for("api.dashboard"))
        else:
            flash("Login incorrect")
    return render_template("login.html")

@api_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("api.login"))

# --- Media
@api_blueprint.route("/assets", methods=["GET"])
@login_required
def list_assets():
    assets = Asset.query.all()
    return render_template("assets.html", assets=assets)

@api_blueprint.route("/assets/upload", methods=["POST"])
@login_required
def upload_asset():
    file = request.files.get("file")
    config = load_config()
    if not file:
        return "No file", 400
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in config['whitelist_exts']:
        return "Extension non autorisée", 400
    filename = os.urandom(4).hex() + "_" + file.filename
    path = os.path.join(config['media_dir'], filename)
    file.save(path)
    size = os.path.getsize(path)
    asset = Asset(filename=filename, original_name=file.filename, path=path, type=guess_type(ext), size_bytes=size)
    db.session.add(asset)
    db.session.commit()
    generate_thumbnail(asset)
    return redirect(url_for("api.list_assets"))

def guess_type(ext):
    if ext in [".jpg", ".jpeg", ".png", ".webp"]:
        return "image"
    elif ext in [".mp4", ".mkv"]:
        return "video"
    elif ext in [".mp3", ".aac", ".wav"]:
        return "audio"
    else:
        return "web"

@api_blueprint.route("/assets/<int:asset_id>/delete", methods=["POST"])
@login_required
def delete_asset(asset_id):
    asset = Asset.query.get(asset_id)
    if asset:
        try:
            if os.path.exists(asset.path):
                os.remove(asset.path)
            if asset.thumb_path and os.path.exists(asset.thumb_path):
                os.remove(asset.thumb_path)
            db.session.delete(asset)
            db.session.commit()
        except Exception as e:
            return str(e), 500
    return redirect(url_for("api.list_assets"))

@api_blueprint.route("/assets/<int:asset_id>/transcode", methods=["POST"])
@login_required
def transcode_asset(asset_id):
    asset = Asset.query.get(asset_id)
    enqueue_transcode(asset)
    return jsonify({"ok": True})

@api_blueprint.route("/assets/thumbs/<filename>")
@login_required
def asset_thumb(filename):
    config = load_config()
    return send_from_directory(config['thumb_dir'], filename)

# --- Playlists, Schedules, Settings, Logs: à compléter (idem pattern ci-dessus)