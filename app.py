from flask import Flask, render_template, request, jsonify
import psycopg2
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from flask_jsglue import JSGlue
from queries import *
import requests


app = Flask(__name__)
jsglue = JSGlue(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("login.html")


@app.route('/players', methods=['GET', 'POST'])
def login():
    if request.method == "POST":

        username = request.form.get("uname")
        userpass = request.form.get("upass")
        usernamedb = ""
        userpassdb = ""

        while not(username == usernamedb and userpass == userpassdb):

            username = request.form.get("uname")
            userpass = request.form.get("upass")

            userinfo = get_user(username)

            usernamedb = userinfo[0][1]
            userpassdb = userinfo[0][2]
        return(render_template("players.html", teams=teams, players=all_players))


@app.route('/players/<team_name>')
def update_players_list(team_name):
    if team_name == "All":
        players = all_players
    else:
        players = get_team_players(team_name.replace(" ", "_"))

    team = {
        "name": team_name,
        "players": players
    }

    return team


@app.route('/update_player_info/<player_name>')
def update_players_info(player_name):
    player_info = get_player_info(player_name)
    return player_info


@app.route('/update_player_stats/<player_name>')
def update_players_stats(player_name):
    player_stats = get_player_stats(2020, player_name)
    return player_stats


'''
@app.route('/populate_graph/<player_name>')
def populate_graph(player_name):
    seasonal_stats = get_seasonal_stats(2020, player_name)
    return seasonal_stats
'''

if __name__ == "__main__":
    app.run(debug=True)
