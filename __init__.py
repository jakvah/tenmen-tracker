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
        connection = dbi.get_database_connection()
        result = dbi.search_table(connection,"matches","match_id",int(searchbox),"match_id")

        return jsonify(result)
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
            
        num_matches = dbi.get_number_of_matches(conn)
        num_players = dbi.get_number_of_players(conn)

        return render_template("tenman/tenman_landing.html",navbar_status=navbar_status,top_players=top_players,num_matches=num_matches,num_players=num_players,threshold=PLAYER_THRESHOLD)

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
    try:
        navbar_status = ["","","active"]
        from match_extraction import popflash_scraper as ps
        match = ps.get_match_data(match_id)
        return render_template("tenman/match_page.html",match=match,navbar_status=navbar_status)
    except Exception as e:
        return str(e)
@app.route("/tenman/add_match", methods=["GET","POST"]) 
def add_pop_match():
    try:
        if request.method == "GET":
            return "Dissallowed, GET"
        elif request.method == "POST":
            
            try:
                from database_management import db_interaction as dbi
            except Exception as e:
                return "db_interaction Import failed: " +  str(e)
            """
            try:
                from database_management import database_exceptions
            except Exception as e:
                return "db_exceptions Import failed: " +  str(e)
            """
            try:
                from match_extraction import popflash_scraper as ps
            except Exception as e:
                return "ps Import failed: " +  str(e)           
            
            try:
                pop_id = request.form["pop_id"]
                pop_match = ps.get_match_data(pop_id)
                            
                conn = dbi.get_database_connection()
                dbi.add_match_data(conn,pop_match)

                flash_str = "Added match " + str(pop_id) + " and updated player data."
                flash(flash_str)                   
                return redirect("/tenman")
            
                
            except Exception as e:
                return str(e)
            
            
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True)
