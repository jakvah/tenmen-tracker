# -*- coding: utf-8 -*- 
from flask import Flask,render_template,Markup,request,redirect,flash

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
    
@app.route("/tenman")
def tenman_index():
    
    try:
        try:
            from database_management import db_interaction as dbi
            #from match_extraction.Player import Player
        except Exception as e:
            return "db_interaction Import failed: " +  str(e)
        try:
            from match_extraction import popflash_scraper as ps
        except Exception as e:
            return "ps Import failed: " +  str(e)
        
        if dbi.get_number_of_players(dbi.get_database_connection()) == 0:
            return render_template("tenman/navbar.html")
        try:
            conn = dbi.get_database_connection()
            top_players = dbi.get_top_players(conn,threshold=1)
            num_matches = dbi.get_number_of_matches(conn)
            num_players = dbi.get_number_of_players(conn)
            player_nicks = []
            """
            for i in range(len(top_players)):
                try:
                    p = top_players[i]
                    nick = (p.get_nick())
                    #nick_uni = unicode(nick,"utf-8")
                    player_nicks.append(nick)
                except Exception as e:
                    return "Norsk alfa suger: " + str(e) + " :" + str(p) #+type(nick_uni)            """


            return render_template("tenman/tenman_landing.html",top_players=top_players,num_matches=num_matches,num_players=num_players)
        except Exception as e:
            return "failed in get top players " +  str(e)

    except Exception as e:
        return "failed:" + str(e)

@app.route("/tenman/user/<pop_id>")
def user_page(pop_id):
    try:
        from database_management import db_interaction as dbi
            #from match_extraction.Player import Player
    except Exception as e:
        return "db_interaction Import failed: " +  str(e)

    try:
        p = dbi.get_player_data(int(pop_id))
    
        return render_template("/tenman/user_profile.html",player=p)
    except Exception as e:
        return "Failed big: " + str(e)
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
