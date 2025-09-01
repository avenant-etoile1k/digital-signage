import os
import argparse
from flask import Flask
from .settings import load_config
from .models import db, init_db, create_default_admin
from .auth import login_manager
from .api import api_blueprint
from .player_api import player_blueprint
from .ws import ws_sock
from .scheduler import scheduler
from .utils import setup_logging

def create_app():
    app = Flask(__name__, static_folder="static")
    config = load_config()
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'supersecret')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{config['db_path']}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = config['media_dir']
    app.config['MAX_CONTENT_LENGTH'] = config['max_upload_size_mb'] * 1024 * 1024

    db.init_app(app)
    login_manager.init_app(app)
    ws_sock.init_app(app)
    app.register_blueprint(api_blueprint)
    app.register_blueprint(player_blueprint)
    app.register_blueprint(ws_sock.sock_bp)

    setup_logging(config['log_dir'], config['log_level'])
    scheduler.init_app(app)
    scheduler.start()

    return app

app = create_app()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--init-db', action='store_true')
    parser.add_argument('--create-admin', action='store_true')
    args = parser.parse_args()

    if args.init_db:
        with app.app_context():
            init_db()
        print("DB initialisée.")
    elif args.create_admin:
        with app.app_context():
            create_default_admin()
        print("Admin créé.")
    else:
        app.run(host="0.0.0.0", port=8080)