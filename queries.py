import psycopg2
import requests
import os
os.environ['DATABASE_URL'] = "postgres://einxqnjrzxddcq:6ad81225d1b2782fd7ba50c04b9e65f2acc9b03cc7f41999c7b99a3e756afad1@ec2-23-23-162-138.compute-1.amazonaws.com:5432/d96rlt79js3sp9"
DATABASE_URL = os.environ['DATABASE_URL']
print(DATABASE_URL)
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
#conn = psycopg2.connect(database="postgres", user='postgres', password='password', host='localhost', port='5432')

# Creating a cursor object using the cursor() method
cursor = conn.cursor()

# Executing an MYSQL function using the execute() method
cursor.execute("select version()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print("Connection established to: ", data)


def get_user(username):
    cursor.execute("SELECT * FROM accounts WHERE username=(%s)", (username,))
    userinfo = cursor.fetchall()
    return userinfo


def clean_up_list(list):
    for i in range(len(list)):
        list[i] = list[i][0].replace("_", "'")
    list.sort()
    return(list)


def get_team_players(team):
    cursor.execute(
        "SELECT concat(first_name, ' ', last_name) AS full_name FROM Players_2020 where is_active=TRUE and team='"+team+"'")
    team = cursor.fetchall()
    team = clean_up_list(team)
    return(team)


def get_teams():
    cursor.execute("SELECT DISTINCT team FROM Players_2020;")
    teams = cursor.fetchall()
    for i in range(len(teams)):
        teams[i] = teams[i][0].replace("_", " ")
    teams.sort()
    return(teams)


def get_all_players():
    cursor.execute(
        "SELECT concat(first_name, ' ', last_name) AS full_name FROM Players_2020 where is_active=TRUE;")
    all_players = cursor.fetchall()
    all_players = clean_up_list(all_players)
    return(all_players)


def get_player_info(fullname):
    fullname = fullname.replace("'", "_")
    cursor.execute("SELECT concat(first_name, ' ', last_name) as fullname, team, player_num, player_pos, image FROM Players_2020 where is_active=TRUE and concat(first_name, ' ', last_name)='"+fullname+"';")
    player = cursor.fetchall()
    player = list(player[0])
    player[0] = player[0].replace("_", "'")
    player[1] = player[1].replace("_", " ")
    player = {
        "name": player[0],
        "team": player[1],
        "number": player[2],
        "position": player[3],
        "image link": player[4]
    }
    return(player)


def get_player_id(fullname):
    fullname = fullname.replace("'", "_")
    cursor.execute(
        "SELECT player_id FROM Players_2020 where is_active=TRUE and concat(first_name, ' ', last_name)='"+fullname+"';")
    id = cursor.fetchall()
    id = id[0][0]
    return(id)


def get_player_stats(season, fullname):
    id = get_player_id(fullname)
    stats_url = "https://www.balldontlie.io/api/v1/season_averages?season={}&player_ids[]={}".format(
        season, id)

    stats = requests.get(stats_url)
    stats = stats.json()
    stats = stats['data']
    stats = stats[0]
    if stats:
        final = stats
        avgs = get_seasonal_stats(season, fullname)
        final.update(avgs)
    else:
        print("no stats for season:{} and id{}".format(season, id))
        final = 0
    return final


def get_seasonal_stats(season, fullname):
    fullname = fullname.replace("'", "_")
    query = "SELECT ppg_{0}::float, rpg_{0}::float, apg_{0}::float, ppg_{1}::float, rpg_{1}::float, apg_{1}::float, ppg_{2}::float, rpg_{2}::float, apg_{2}::float\
                       FROM Players_2020\
                       where is_active=TRUE\
                       and concat(first_name, ' ', last_name)='{3}';".format(season, season-1, season-2, fullname)
    cursor.execute(query)
    stats = cursor.fetchall()
    if stats:
        stats = list(stats)[0]
        stats = {
            "ppg_"+str(season): stats[0],
            "rpg_"+str(season): stats[1],
            "apg_"+str(season): stats[2],
            "ppg_"+str(season-1): stats[3],
            "rpg_"+str(season-1): stats[4],
            "apg_"+str(season-1): stats[5],
            "ppg_"+str(season-2): stats[6],
            "rpg_"+str(season-2): stats[7],
            "apg_"+str(season-2): stats[8]
        }
    else:
        print("no "+str(season)+" stats for this player")
        stats = 0
    return stats


teams = get_teams()
all_players = get_all_players()

hawks = get_team_players("Atlanta_Hawks")
celtics = get_team_players("Boston_Celtics")
nets = get_team_players("Brooklyn_Nets")
hornets = get_team_players("Charlotte_Hornets")
bulls = get_team_players("Chicago_Bulls")
cavaliers = get_team_players("Cleveland_Cavaliers")
mavericks = get_team_players("Dallas_Mavericks")
nuggets = get_team_players("Denver_Nuggets")
pistons = get_team_players("Detroit_Pistons")
warriors = get_team_players("Golden_State_Warriors")
rockets = get_team_players("Houston_Rockets")
pacers = get_team_players("Indiana_Pacers")
clippers = get_team_players("LA_Clippers")
lakers = get_team_players("Los_Angeles_Lakers")
grizzlies = get_team_players("Memphis_Grizzlies")
heat = get_team_players("Miami_Heat")
bucks = get_team_players("Milwaukee_Bucks")
timberwolves = get_team_players("Minnesota_Timberwolves")
pelicans = get_team_players("New_Orleans_Pelicans")
knicks = get_team_players("New_York_Knicks")
thunder = get_team_players("Oklahoma_City_Thunder")
magic = get_team_players("Orlando_Magic")
seventysixers = get_team_players("Philadelphia_76ers")
suns = get_team_players("Phoenix_Suns")
trailblazers = get_team_players("Portland_Trail_Blazers")
kings = get_team_players("Sacramento_Kings")
spurs = get_team_players("San_Antonio_Spurs")
raptors = get_team_players("Toronto_Raptors")
jazz = get_team_players("Utah_Jazz")
wizards = get_team_players("Washington_Wizards")
