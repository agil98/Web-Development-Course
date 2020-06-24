import os
from flask import Flask, session, redirect, render_template, request, jsonify
from flask_socketio import SocketIO
from flask_assets import Environment, Bundle
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)
socketio.run(app, debug=True)

assets = Environment(app)
assets.url = app.static_url_path
assets.debug = True

scss = Bundle('sass/signin.scss', filters='pyscss', output='gen/all.css')
assets.register('scss_all', scss)

channels = { 1: "First", 2: "Second", 3:"Third"}

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
    return render_template("index.html", channels=channels)

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    session.clear()
    if request.method == 'POST':
        username = request.form.get("display_name")
        session['username'] = username
        session.permanent = True
        return redirect("/")
    else:
        return render_template("signin.html")

@app.route('/channel', methods=["POST", "GET"])
def channel():
    return render_template('channel.html')

@socketio.on('sending message')
def send_message(json, methods=['GET', 'POST']):
    username = session["username"]
    message = json["message"]
    socketio.emit('message sent', {'username': username, 'message': message})
