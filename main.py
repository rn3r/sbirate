#Imports 
import os
from flask import Flask, send_file, render_template, request, session, redirect, jsonify, escape, Blueprint, abort
from flask_cors import CORS, cross_origin
from threading import Thread
from flask_wtf.csrf import CSRFProtect
from flask_wtf.csrf import CSRFError

#App Setup
app = Flask(__name__)
csrf = CSRFProtect(app)
csrf.init_app(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = "Na&1bTaFatlYz2E0" # Change to b64 
app.config["TEMPLATES_AUTO_RELOAD"] = True

#Importing Routes
from routes import api, front

all_routes = [api.f_, front.f_]
load = 0

for route in all_routes:
    load += 1
    try:
        app.register_blueprint(route)
        print(f" * Load {route.name}{' '*(15-len(route.name))}| Success | {load/len(all_routes):.2%} Loaded")
    except:
        print(f" * Load {route.name}{' '*(15-len(route.name))}| Failed  | {load/len(all_routes):.2%} Loaded")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", session=session), 404

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    print(f"{request.access_route[-1]} had a CSRF error")
    return "CSRF error, please refresh", 403

#Starting App
os.system("cls")
server = Thread(target = app.run(host = '0.0.0.0', port=8000))
server.start()
