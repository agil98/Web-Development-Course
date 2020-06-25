import os
from flask import Flask, session, redirect, render_template, request, jsonify
from flask_socketio import SocketIO
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)
socketio.run(app, debug=True)

channels = {}
current_messages = []
users = []

def login_required(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None:
            return redirect("/signin")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    print(channels)
    return render_template("index.html", channels=channels.keys())

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    session.clear()
    if request.method == 'POST':
        username = request.form.get("display_name")
        if username not in users:
            users.append(username)
        session['username'] = username
        session.permanent = True
        return redirect("/")
    else:
        return render_template("signin.html")

@app.route('/layout', methods=["GET"])
def layout():
    return render_template('layout.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('signin.html')

@app.route('/create', methods=["POST", "GET"])
def create():
    if request.method=='POST':
        key = request.form.get("name")
        if key in channels.keys():
            return render_template('create.html', already_exists = True)
        else:
            current_messages = []
            channels[key] = current_messages
            return render_template('index.html', channels=channels.keys())
    return render_template('create.html', already_exists = False)


@app.route('/channel/<string:name>', methods=["POST", "GET"])
def channel(name):
    current_messages = channels[name]
    session["current_channel"] = name
    return render_template('channel.html', messages = current_messages, name = name)

@socketio.on('sending message')
def send_message(json, methods=['GET', 'POST']):
    username = session["username"]
    message = json["message"]
    timestamp = json["timestamp"]
    current_messages.append([username, message, timestamp])
    channels[session["current_channel"]] = current_messages
    socketio.emit('message sent', {'username': username, 'message': message, 'timestamp': timestamp})