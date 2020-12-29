# -*- coding: utf-8 -*- 
from flask import Flask,render_template,Markup,request,redirect,flash,jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/pdf_viewer/<filename>")
def show_pdf(filename):    
    try:
        """
        html_string = '<iframe src="' + "{" + "{" +'url_for' + "('static',filename='pdfs/" + str(filename) +".pdf')" + "}"+ '}"' + ' width="100%" height="100%">You browswer doesnt support PDFs. Consider downloading the PDF </iframe>'
        tag = Markup(html_string)
        """
        location = "pdfs/" + str(filename) + ".pdf"
        return render_template("pdf_viewer.html",link = location)
    except Exception as e:
        return str(e)

@app.route("/tenman/nothing")
def nothing():
    navbar_status = ["","",""]
    return render_template("tenman/no_players.html",navbar_status=navbar_status)

@app.route("/tenman/players")
def players():
    from database_management import db_interaction as dbi
    conn = dbi.get_database_connection()
    num_players = dbi.get_number_of_players(conn)
    navbar_status = ["","active",""]
    return render_template("tenman/players.html",num_players=num_players,navbar_status=navbar_status)

@app.route("/livesearch",methods=["POST","GET"])
def livesearch():
    try:
        from database_management import db_interaction as dbi

        searchbox = request.form.get("text")
        connection = dbi.get_database_connection()
        result = dbi.search_table(connection,"players","nick",searchbox,"pop_id","nick","hltv_rating","img_url","wins","losses")

        return jsonify(result)
    except Exception as e:
        return jsonify(str(e))


@app.route("/livesearch_matches",methods=["POST","GET"])
def livesearch_match():
    try:
        from database_management import db_interaction as dbi

        searchbox = request.form.get("text")
        connection1 = dbi.get_database_connection()
        connection2 = dbi.get_database_connection()
        
        if searchbox == "":
            r = dbi.search_table(connection1,"matches","match_id",searchbox,"match_id","map_name","map_img_url","date")
            return jsonify(r) 
        result_id = dbi.search_table(connection1,"matches","match_id",searchbox,"match_id","map_name","map_img_url","date")
        result_map = dbi.search_table(connection2,"matches","map_name",searchbox,"match_id","map_name","map_img_url","date")
        result_date = dbi.search_table(connection2,"matches","date",searchbox,"match_id","map_name","map_img_url","date")

        results = result_id + result_date + result_map
        return jsonify(results)
    except Exception as e:
        return jsonify(str(e))

@app.route("/tenman")
def tenman_index():
    PLAYER_THRESHOLD = 6
    navbar_status = ["active","",""]
    try:
        try:
            from database_management import db_interaction as dbi
        except Exception as e:
            return "db_interaction Import failed: " +  str(e)
        try:
            from match_extraction import popflash_scraper as ps
        except Exception as e:
            return "ps Import failed: " +  str(e)
        
        if dbi.get_number_of_players(dbi.get_database_connection()) == 0:
            return render_template("tenman/no_players.html",num_matches=0,num_players=0)
        try:
            conn = dbi.get_database_connection()

            top_players = dbi.get_top_players(conn,threshold=PLAYER_THRESHOLD)
        except Exception as e:
            return "failed in get top players " +  str(e)

        try:   
            num_matches = dbi.get_number_of_matches(conn)
            num_players = dbi.get_number_of_players(conn)
        except Exception as e:
            return "asd" + str(e)
        
        try:
            # Get latest match
            data = dbi.get_table_data(conn,"matches")
            last_match = data[len(data)-1]
            from match_extraction.Match import Match
            from match_extraction.Team import Team
            from match_extraction.Player import Player
            latest_match = Match(int(last_match[0]),team1=Team(),team2=Team(),map_img_url=last_match[2],date=last_match[3],map_name=last_match[1])
        except Exception as e:
            return "get latest; " + str(e)        
        return render_template("tenman/tenman_landing.html",navbar_status=navbar_status,top_players=top_players,num_matches=num_matches,num_players=num_players,latest_match=latest_match,threshold=PLAYER_THRESHOLD)

    except Exception as e:
        return "failed:" + str(e)

@app.route("/tenman/user/<pop_id>")
def user_page(pop_id):
    navbar_status = ["","active",""]
    try:
        from database_management import db_interaction as dbi
            #from match_extraction.Player import Player
    except Exception as e:
        return "db_interaction Import failed: " +  str(e)

    try:
        p = dbi.get_player_data(int(pop_id))
    
        return render_template("/tenman/user_profile.html",player=p,navbar_status=navbar_status)
    except Exception as e:
        return "Failed big: " + str(e)

@app.route("/tenman/matches")
def matches():
    try:
        from database_management import db_interaction as dbi
        
        navbar_status = ["","","active"]
        conn = dbi.get_database_connection()
        num_matches = dbi.get_number_of_matches(conn)
        
        return render_template("/tenman/matches.html",navbar_status=navbar_status,num_matches=num_matches)
    except Exception as e:
        return str(e)

@app.route("/tenman/match/<match_id>")
def match_page(match_id):
    # New
    navbar_status = ["","","active"]
    return render_template("tenman/loading_match.html",navbar_status=navbar_status,match_id=match_id)


@app.route("/tenman/loading_match")
def loading():
    navbar_status = ["","","active"]
    return render_template("tenman/loading_match.html",navbar_status=navbar_status)

@app.route("/get_match_data/<match_id>")
def get_match_data(match_id):
    try:
        try:
            from match_extraction import popflash_scraper as ps
            from database_management import db_interaction as dbi
            from match_extraction.Match import Match
            from match_extraction.Team import Team
            from match_extraction.Player import Player
        except Exception as e:
            return "Failed importing modules: " + str(e)

        navbar_status = ["","","active"]
        match = ps.get_match_data(match_id)

        # Get team balance ratings
        team1 = match.get_team_1()
        team2 = match.get_team_2()

        team1_total = 0
        team2_total = 0

        his_avg_team_1 = Team()
        his_avg_team_2 = Team()

        for player in team1:
            p1 = dbi.get_player_data(int(player.get_pop_id()))
            team1_total += p1.get_hltv_rating()
            his_avg_team_1.add_player(p1)

        for player in team2:
            p2 = dbi.get_player_data(int(player.get_pop_id()))
            team2_total += p2.get_hltv_rating()
            his_avg_team_2.add_player(p2)

        
        team1_avg_rating = float(team1_total) / 5.0
        team2_avg_rating = float(team2_total) / 5.0

        team1_percentage = 100*(team1_avg_rating / (team1_avg_rating + team2_avg_rating)) 
        team2_percentage = 100*(team2_avg_rating / (team1_avg_rating + team2_avg_rating)) 

        return render_template("tenman/match_page.html",
                match=match,
                navbar_status=navbar_status,
                team1_avg_rating=team1_avg_rating,
                team2_avg_rating=team2_avg_rating,
                team1_percentage=team1_percentage,
                team2_percentage=team2_percentage,
                his_avg_team_1 = his_avg_team_1,
                his_avg_team_2 = his_avg_team_2
            )
    except Exception as e:
        return str(e)

@app.route("/test")
def test():
    try:
        return render_template("test.html") 
    except Exception as e:
        return str(e)
@app.route("/tenman/add_match", methods=["GET","POST"]) 
def add_pop_match():
    try:
        if request.method == "GET":
            return "Im sorry bro, you can't access this endpoint this way."
        elif request.method == "POST":            
            try:
                from database_management import db_interaction as dbi
            except Exception as e:
                return "Failed when importing the database management module: " +  str(e)
            
            try:
                from match_extraction import popflash_scraper as ps
            except Exception as e:
                return "Failed when importing the webscraper " +  str(e)          
            
            try:                
                pop_id = request.form["pop_id"]
                conn = dbi.get_database_connection()
                if dbi.exists_in_table(conn,"matches",int(pop_id)):
                    flash_str = "Match " + str(pop_id) + " has already been added to the database! Player data has not been updated."
                    flash(flash_str) 
                    return redirect("/tenman")        
                else:
                    pop_match = ps.get_match_data(pop_id)            
                    dbi.add_match_data(conn,pop_match)

                    flash_str = "Successfully added match " + str(pop_id) + " and updated player data."
                    flash(flash_str)                   
                    return redirect("/tenman")                
                
            except Exception as e:
                return str(e)
            
            
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True)
