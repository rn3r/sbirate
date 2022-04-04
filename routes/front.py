#Imports
from flask import Flask, send_file, render_template, request, session, redirect, jsonify, escape, Blueprint, abort, current_app
from flask_cors import CORS, cross_origin
from flask_wtf.csrf import CSRFProtect
from flask_wtf.csrf import CSRFError
from flask.globals import current_app
import json

f_ = Blueprint('front',__name__)
csrf = CSRFProtect(current_app)

def queryJson(query, key, data):
    if query in [a[key] for a in data]:
        for a in data:
            if a[key] == query:
                return a
    return False

@f_.route('/', methods=["GET", "POST"])
@csrf.exempt
def home():
    return render_template("home.html", session=session)

@f_.route('/episodes', methods=["GET", "POST"])
@csrf.exempt
def eps():
    with open("static/seasons.json", "r") as f:
        seasons = json.load(f)
    return render_template("browse.html", session=session, episodes=seasons)

@f_.route('/episodes/<season>', methods=["GET", "POST"])
@csrf.exempt
def szneps(season):
    try:
        with open("static/episodes.json", "r") as f:
            episodes_data = json.load(f)[season]
    except Exception as e:
        print(e)
        return render_template("404.html"), 404

    episodes = []

    for a in episodes_data:
        episodes.append(episodes_data[a])

    return render_template("browse.html", session=session, episodes=episodes)

@f_.route('/watch/<season>/<episode>', methods=["GET", "POST"])
@csrf.exempt
def watch(season, episode):
    try:
        with open("static/episodes.json", "r") as f:
            data = json.load(f)[season][episode]
    except Exception as e:
        print(e)
        return render_template("404.html"), 404

    with open("static/episodes.json", "r") as f:
        edata = json.load(f)[season]

    szn = []
    passed = False

    for a in edata:
        if passed:
            if len(szn) == 0:
                nextep = f"/watch/{season}/{a}"
            szn.append(edata[a])
        if a == episode:
            passed = True

    if len(szn) == 0:
        seasonNum = int(season.split("s")[1])+1
        seasonNum = seasonNum%12
        if seasonNum == 0:
            seasonNum = 1
        s = f"s{seasonNum}"
        with open("static/episodes.json", "r") as f:
            edata = json.load(f)[s]

        for a in edata:
            if len(szn) == 0:
                nextep = f"/watch/{s}/{a}"
            szn.append(edata[a])

    return render_template("player.html", session=session, episodes=data, inSeason=szn, nextep=nextep)