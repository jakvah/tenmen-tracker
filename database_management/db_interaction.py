"""
Module for interacting with the database
"""

import sys
sys.path.append("..")

import MySQLdb
import os.path
if __name__ == "__main__":

    from database_exceptions import *
    from match_extraction.Player import Player
    from match_extraction.Match import Match
    from match_extraction.Team import Team
    from match_extraction.Outcome import *
else:
    from database_management.database_exceptions import *


DATABASE_LOGIN_DETAILS = {
	"host":"localhost",
	"user":"root",
	"password":"mysqlroot123",
	"database":"tenmandb"
}
def get_database_connection():
    try:
        db_conn = MySQLdb.connect(DATABASE_LOGIN_DETAILS["host"],DATABASE_LOGIN_DETAILS["user"],DATABASE_LOGIN_DETAILS["password"],DATABASE_LOGIN_DETAILS["database"])
        return db_conn
    except Exception as e:
        print("Could not establish connection to the database. Is the server running?")
        return None
def table_exists(dbconn,tablename):
    	dbcur = dbconn.cursor()
    	dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    	if dbcur.fetchone()[0] == 1:
        	dbcur.close()
        	return True

    	dbcur.close()
    	return False

def get_table_data(dbconn, tablename):
    cur = dbconn.cursor()
    sql = "SELECT * FROM " + tablename
    cur.execute(sql)
    dataset = cur.fetchall()
    cur.close()

    return dataset

def exists_in_table(dbconn,tablename,search_item):
    data = get_table_data(dbconn,tablename)
    for i in range(len(data)):
        if search_item == data[i][0]:
            return True

def add_match_id(dbconn,match_id):
    if exists_in_table(dbconn,"matches",match_id):
        raise ElementExistsInTableError
    if not table_exists(dbconn,"matches"):
        raise TablesDoesNotExistError

    else:
        dbcur = dbconn.cursor()
        query = "INSERT INTO " + "matches" + """(match_id) VALUES (%s)"""
        dbcur.execute(query,[match_id])
        dbconn.commit()
        dbcur.close()

# Adds new player, with stats = 0
def add_player(dbconn,player_id,player_nick):
    if exists_in_table(dbconn,"players",int(player_id)):
        raise ElementExistsInTableError
    try:
        db_cur = dbconn.cursor()
        query = "INSERT INTO players " + \
            """(pop_id,nick,kills,deaths,assists,f_assists,adr,hltv_rating,hs_per,clutck_kills,bombs_planted,bombs_defused,kd_ratio,wins,losses) \
                VALUES (%s,%s,0,0,0,0,0,0,0,0,0,0,0,0,0)"""
        db_cur.execute(query,[player_id,player_nick])
        dbconn.commit()
    except Exception as e:
        raise AddingPlayerError

# Takes match object and updates player data from the match
def add_match_data(dbconn,match):
    try:
        add_match_id(dbconn,match.get_match_id())
        
        # Add determine outcome
        winning_team = match.get_winner()
        loosing_team = match.get_looser()
        for player in winning_team:
            update_player_data(dbconn,player,won=True)
        for player in loosing_team:
            update_player_data(dbconn,player,won=False)
    except ElementExistsInTableError:
        print("Match already exists, will not add copy")

# Takes instance of Player class and updates stats for Player.pop_id. 
def update_player_data(dbconn,player,won):
    db_cur = dbconn.cursor()
    player_id = player.popflash_id
    if not exists_in_table(dbconn,"players",int(player_id)):
        add_player(dbconn,player_id,player.nick_name)

    query = "SELECT * FROM players WHERE pop_id = " + str(player_id)
    db_cur.execute(query)
    dataset = db_cur.fetchall()

    
    # Assign new values
    new_nick = player.nick_name
    new_kills = int(player.kills) + int(dataset[0][2])
    new_deaths = int(player.deaths) + int(dataset[0][3])
    new_assists = int(player.assists) + int(dataset[0][4])
    new_f_assists = int(player.flash_assists) + int(dataset[0][5])
    new_adr = float(player.adr) + float(dataset[0][6]/2)
    new_hltv_rating = (float(player.hltv_rating) + float(dataset[0][7]))/2
    new_hs_per = (float(player.hs_percentage) + float(dataset[0][8]))/2
    new_ck = int(player.clutch_kills) + int(dataset[0][9])
    new_bombs_planted = int(player.bombs_planted) + int(dataset[0][10])
    new_bombs_defused = int(player.bombs_defused) + int(dataset[0][11])
    try:
        new_kd_ratio = new_kills / new_deaths
    except ZeroDivisionError:
        new_kd_ratio = 0
    
    if won:
        new_wins = dataset[0][13] +1
        new_losses = dataset[0][14]
    else:
        new_wins = dataset[0][13]
        new_losses = dataset[0][14] +1

    new_vals = [new_nick,new_kills,new_deaths,new_assists,new_f_assists,new_adr,new_hltv_rating,new_hs_per,new_ck,new_bombs_planted,new_bombs_defused,new_kd_ratio,new_wins,new_losses] + [player_id]

    query = "UPDATE players SET nick = %s, kills = %s,deaths =%s,assists = %s,f_assists=%s,adr=%s,hltv_rating=%s,hs_per=%s,clutck_kills=%s,bombs_planted=%s,bombs_defused=%s,kd_ratio=%s,wins=%s,losses=%s WHERE pop_id = %s"
    db_cur.execute(query,new_vals)
    dbconn.commit()
        
    db_cur.close()


if __name__ == "__main__":
    p = Player(1123196,nick="Jossen",kills=10,deaths=1,assists=0,f_assists=2,adr=49,hltv_rating=1.34,hs_percentage=0.34,ck=0,bombs_planted=2,bombs_defused=3)
    print(p)

    db_conn = get_database_connection()
    try:
        add_player(db_conn,"638279","jakvah")
    except ElementExistsInTableError:
        print("Players exists")
    try:
        add_player(db_conn,1123196,"Jossen")
    except ElementExistsInTableError:
        print("Players exists")
    update_player_data(db_conn,p,True)
