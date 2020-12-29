# -*- coding: utf-8 -*- 

"""
Module for interacting with the database
"""

import sys
sys.path.append("..")

import MySQLdb
import os.path

from database_exceptions import *

DATABASE_LOGIN_DETAILS = {
	"host":"localhost",
	"user":"root",
	"password":"mysqlroot123",
	"database":"tenmandb"
}

# Returns a datbase connection object.
def get_database_connection():
    try:
        db_conn = MySQLdb.connect(DATABASE_LOGIN_DETAILS["host"],DATABASE_LOGIN_DETAILS["user"],DATABASE_LOGIN_DETAILS["password"],DATABASE_LOGIN_DETAILS["database"],use_unicode=True, charset="utf8")
        return db_conn
    except Exception as e:
        print("Could not establish connection to the database. Is the server running?")
        return None

# Checks if table exists
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

# Searches table for a target equal to target_value. Returns elements specified by *select
def search_table(dbconn,table,target,target_value,*select):
    cursor = dbconn.cursor()

    # Create query for cursor
    query = "SELECT "

    for index, value in enumerate(select):
        if index == (len(select)-1):
            query += str(value)
        else:
            query += str(value) + ","
    
    query += " FROM " + str(table) + " WHERE " + str(target) \
        + " LIKE '" + str(target_value) + "%' order by " + str(target)
    
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

# Returns table data as 2 dimmensional list (list of lists)
def get_table_data(dbconn, tablename):
    cur = dbconn.cursor()
    sql = "SELECT * FROM " + tablename
    cur.execute(sql)
    dataset = cur.fetchall()
    cur.close()

    return dataset

# Checks if search_item exists in tablename
def exists_in_table(dbconn,tablename,search_item):
    data = get_table_data(dbconn,tablename)
    for i in range(len(data)):
        if search_item == data[i][0]:
            return True

# Adds match id, map, map image url and date and day
def add_match_id(dbconn,match):
    if exists_in_table(dbconn,"matches",int(match.get_match_id())):
        raise ElementExistsInTableError
    if not table_exists(dbconn,"matches"):
        raise TablesDoesNotExistError
    else:
        dbcur = dbconn.cursor()
        query = "INSERT INTO " + "matches" + """(match_id,map_name,map_img_url,date) VALUES (%s,%s,%s,%s)"""
        dbcur.execute(query,[match.get_match_id(),match.get_map(),match.get_map_img_url(),match.get_date()[4:]])
        dbconn.commit()
        dbcur.close()

# Adds new player, with stats = 0
def add_player(dbconn,player_id,player_nick):
    if exists_in_table(dbconn,"players",int(player_id)):
        raise ElementExistsInTableError
    try:
        db_cur = dbconn.cursor()
        query = "INSERT INTO players " + \
            """(pop_id,nick,kills,deaths,assists,f_assists,adr,hltv_rating,hs_per,clutck_kills,bombs_planted,bombs_defused,kd_ratio,wins,losses,img_url) \
                VALUES (%s,%s,0,0,0,0,0,0,0,0,0,0,0,0,0,"")"""
        db_cur.execute(query,[player_id,player_nick])
        dbconn.commit()
    except Exception as e:
        raise AddingPlayerError

# Takes match object and updates player data from the match
def add_match_data(dbconn,match):
    if exists_in_table(dbconn,"matches",int(match.get_match_id())):
        return
    try:
        add_match_id(dbconn,match)
        
        # Add determine outcome
        if match.is_tie():
            for player in match.team_1:
                update_player_data(dbconn,player,won=False,tie=True)
            for player in match.team_2:
                update_player_data(dbconn,player,won=False,tie=True)
        else:
            winning_team = match.get_winner()
            loosing_team = match.get_looser()
            for player in winning_team:
                update_player_data(dbconn,player,won=True)
            for player in loosing_team:
                update_player_data(dbconn,player,won=False)
    except ElementExistsInTableError:
        raise ElementExistsInTableError


# Adding data parameters for existing matches, where sufficient data has not been stored
def update_match_data(match):
    conn = get_database_connection()
    cur = conn.cursor()
    query = """UPDATE matches SET map_name=%s, map_img_url=%s, date=%s WHERE match_id=%s"""
    values = [match.get_map(),match.get_map_img_url(),match.get_date()[4:],match.get_match_id()]
    cur.execute(query,values)

    conn.commit()
    conn.close()

# Takes instance of Player class and updates stats for Player.pop_id. 
def update_player_data(dbconn,player,won,tie=False):
    first_time = False
    db_cur = dbconn.cursor()
    player_id = player.popflash_id
    if not exists_in_table(dbconn,"players",int(player_id)):
        add_player(dbconn,player_id,player.get_nick())
        first_time = True

    query = "SELECT * FROM players WHERE pop_id = " + str(player_id)
    db_cur.execute(query)
    dataset = db_cur.fetchall()

    # Assign new values
    new_nick = player.get_nick()
    new_kills = int(player.kills) + int(dataset[0][2])
    new_deaths = int(player.deaths) + int(dataset[0][3])
    new_assists = int(player.assists) + int(dataset[0][4])
    new_f_assists = int(player.flash_assists) + int(dataset[0][5])

    if not first_time:
        new_match_total = dataset[0][13] + dataset[0][14] + 1
        new_adr = update_average(float(dataset[0][6]),float(player.get_adr()),new_match_total)
        new_hltv_rating = update_average(float(dataset[0][7]),float(player.get_hltv_rating()),new_match_total)
        new_hs_per = update_average(float(dataset[0][8]),float(player.get_hs_percentage()),new_match_total)
    else:
        new_adr = float(player.adr)
        new_hltv_rating = float(player.hltv_rating)
        new_hs_per = float(player.hs_percentage)

    new_ck = int(player.clutch_kills) + int(dataset[0][9])
    new_bombs_planted = int(player.bombs_planted) + int(dataset[0][10])
    new_bombs_defused = int(player.bombs_defused) + int(dataset[0][11])
    try:
        new_kd_ratio = float(new_kills) / float(new_deaths)
    except ZeroDivisionError:
        new_kd_ratio = 0
    if tie:
        new_wins = dataset[0][13]
        new_losses = dataset[0][14]
    elif won:
        new_wins = dataset[0][13] +1
        new_losses = dataset[0][14]
    elif not won:
        new_wins = dataset[0][13]
        new_losses = dataset[0][14] +1
    
    new_img_url = player.get_img_url()

    new_vals = [new_nick,new_kills,new_deaths,new_assists,new_f_assists,new_adr,new_hltv_rating,new_hs_per,new_ck,new_bombs_planted,new_bombs_defused,new_kd_ratio,new_wins,new_losses,new_img_url] + [player_id]

    query = "UPDATE players SET nick = %s, kills = %s,deaths =%s,assists = %s,f_assists=%s,adr=%s,hltv_rating=%s,hs_per=%s,clutck_kills=%s,bombs_planted=%s,bombs_defused=%s,kd_ratio=%s,wins=%s,losses=%s,img_url=%s WHERE pop_id = %s"
    db_cur.execute(query,new_vals)
    dbconn.commit()
        
    db_cur.close()

def update_average(old_average,new_value,new_total):
    u_1 = float(old_average) * (float(1) / (float(new_total)/float(new_total-1)))
    new_average = u_1 + float(new_value) / float(new_total)
    return new_average
def get_top_players(dbconn,threshold,tablename="players"):
    top_player_ids = []

    table_data = get_table_data(dbconn,tablename)
    num_players = len(table_data)

    for n in range(num_players):
        best_hltv_rating = 0
        best_pop_id = None
        for i in range(len(table_data)):
            pop_id = table_data[i][0]
            wins = table_data[i][13]
            loss = table_data[i][14]
            if pop_id in top_player_ids:
                continue
            
            else:
                hltv_rating = table_data[i][7]
                if hltv_rating > best_hltv_rating:
                    best_hltv_rating = hltv_rating
                    best_pop_id = pop_id
                    
        top_player_ids.append(best_pop_id)

    top_players = []
    for i in top_player_ids:
        p = get_player_data(i)
        if p.get_wins() + p.get_losses() >= threshold:
            top_players.append(p)
    return top_players
        
def get_player_data(player_id,tablename = "players"):
    from ..match_extraction.Player import Player 
    db_con = get_database_connection()
    table_data = get_table_data(db_con,tablename)    
    
    for i in range(len(table_data)):
        pop_id = table_data[i][0]
        if pop_id == player_id:
            nick = table_data[i][1]
            p = Player(player_id,nick=nick)

            p.set_kills(table_data[i][2])
            p.set_deaths(table_data[i][3])
            p.set_assists(table_data[i][4])
            p.set_flash_assists(table_data[i][5])
            p.set_adr(int(table_data[i][6]))
            p.set_hltv_rating(round(table_data[i][7],2))
            p.set_hs_percentage(float(table_data[i][8]))
            p.set_clutch_kills(table_data[i][9])
            p.set_bombs_planted(table_data[i][10])
            p.set_bombs_defused(table_data[i][11])
            p.set_kd_ratio(table_data[i][12])
            p.set_wins(table_data[i][13])
            p.set_losses(table_data[i][14])
            p.set_img_url(table_data[i][15])
    
    return p

def get_number_of_matches(dbconn,tablename="matches"):
    data = get_table_data(dbconn,tablename)
    return len(data)
def get_number_of_players(dbconn,tablename="players"):
    data = get_table_data(dbconn,tablename)
    return len(data)

if __name__ == "__main__":
    from ..match_extraction import popflash_scraper as ps    
    m = ps.get_match_data(1107734)
    update_match_data(m)
    print("Done!")

    """    
    c = get_database_connection()
    data = get_table_data(c,"matches")
    for row in data:
        print(row[0])
    """