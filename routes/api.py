#Imports
from flask import Flask, send_file, render_template, request, session, redirect, jsonify, escape, Blueprint, abort, current_app
from flask_cors import CORS, cross_origin
from flask_wtf.csrf import CSRFProtect
from flask.globals import current_app

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
        
    return render_template("login.html")

@f_.route('/register', methods=["GET", "POST"])
def register():
    if 'sessid' in session:
        return redirect("/")
        
    return render_template("register.html")
