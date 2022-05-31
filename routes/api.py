#Imports
from flask import Flask, send_file, render_template, request, session, redirect, jsonify, escape, Blueprint, abort, current_app
from flask_cors import CORS, cross_origin
from flask_wtf.csrf import CSRFProtect
from flask.globals import current_app
import json
import app_functions

allowed_characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9']
f_ = Blueprint('backend',__name__)
csrf = CSRFProtect(current_app)

def queryJson(query, key, data):
    if str(query) in [a[str(key)] for a in data]:
        for a in data:
            if a[str(key)] == query:
                return a
    return False

@f_.route('/login', methods=["GET", "POST"])
def login():
    if 'sessid' in session:
        return redirect("/")

    if request.method == 'POST':
        #Variables
        with open("data/accounts.json", "r") as f:
            info = json.load(f)
        username = escape(request.form["user"].lower())
        password = escape(request.form["password"])

        #Checking if user exists
        acc = queryJson(username, "username", info)
        if not acc:
            return "This user doesnt exist", 403

        #Getting information
        login_info = queryJson(username, "username", info)
        decrypted = app_functions.CheckPassword(password, login_info['password'])
        if not decrypted:
            return "Invalid password.", 403

        sessid = login_info['sessid']
        session['sessid'] = sessid
        session["username"] = username
        return "success"
        
    return render_template("login.html")

@f_.route('/register', methods=["GET", "POST"])
def register():
    if 'sessid' in session:
        return redirect("/")

    if request.method == 'POST':
        #Request Form Variables
        with open("data/accounts.json", "r") as f:
            info = json.load(f)
            
        username = request.form["user"].lower()
        password = request.form["password"]
        sessid = request.form["sessid"]
        _id = request.form["id"]

        if len(username) < 2 or len(username) > 20:
            return "Your username must be in between 2 and 20 characters length.", 403

        for character in username:
            if character not in allowed_characters:
                return "You can only use letters and numbers in your username.", 403

        if len(password) < 8 or len(password) > 250:
            return "Your password must be in between 8 and 250 characters length.", 403

        if queryJson(username, "username", info):
            return "Username unavailable", 403

        #Encrypt
        password = app_functions.HashPassword(password)
        hashed_pass = app_functions.removeExtraShit(str(password))

        data = {
            "id": int(_id),
            "sessid": sessid,
            "password": hashed_pass,
            "username": username,
            "resume": {
                "data": {
                    "season": 's1',
                    "episode": "e01",
                    "seconds": 0
                },
                "enabled": True
            }
        }

        try:
            with open("data/accounts.json", "r") as f:
                accs = json.load(f)
            with open("data/accounts.json", "w") as f:
                accs.append(data)
                json.dump(accs, f, indent=4)
            session["sessid"] = sessid
            session["username"] = username
        except Exception as e:
            print(e)
            return "Database Error", 403
        
    return render_template("register.html")

@f_.route('/api/player/save-spot', methods=["GET", "POST"])
@csrf.exempt
def saveAPI():
    if 'sessid' not in session:
        return 'no account'

    with open('data/accounts.json', 'r') as f:
        data = json.load(f)

    userdata = queryJson(session['sessid'], 'sessid', data)

    if request.form['episode'] == userdata['resume']['data']['episode'] and request.form['season'] == userdata['resume']['data']['season'] and int(request.form['seconds']) < userdata['resume']['data']['seconds']:
        return 'below past time', 200
    
    userdata['resume']['data'] = {
        'episode': request.form['episode'],
        'season': request.form['season'],
        'seconds': int(request.form['seconds'])
    }

    with open('data/accounts.json', 'w') as f:
        json.dump(data, f, indent=4)

    return 'yep'

@f_.route('/api/player/get-spot', methods=["GET", "POST"])
@csrf.exempt
def getAPI():
    if 'sessid' not in session:
        return 'no account'

    with open('data/accounts.json', 'r') as f:
        data = json.load(f)

    userdata = queryJson(session['sessid'], 'sessid', data)

    return jsonify(userdata['resume']['data'])
