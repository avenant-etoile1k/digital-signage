from flask_sock import Sock
from flask import Blueprint
import threading

ws_sock = Sock()
sock_bp = Blueprint('ws', __name__)

# List of connected player clients
clients = []

@sock_bp.route("/ws/player")
def ws_player(ws):
    clients.append(ws)
    try:
        while True:
            data = ws.receive()
            # handle incoming messages if needed
    except:
        pass
    finally:
        clients.remove(ws)

def send_command(command, payload=None):
    for ws in clients:
        ws.send({"command": command, "payload": payload})