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
            pop_id = request.form["pop_id"]
            # Add match ID to match ID table
            # Get match object from ID using get_match_data
            return redirect("/tenman")
            
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True)
