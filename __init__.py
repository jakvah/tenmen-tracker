from flask import Flask,render_template,Markup,request,redirect

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
        return render_template("tenman/tenman_landing.html")
    except Exception as e:
        return "failed:" + str(e)

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
                return "done"
            
                
            except Exception as e:
                return str(e)


            
            
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True)
