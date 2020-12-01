from flask import Flask,render_template,Markup
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

        
if __name__ == "__main__":
    app.run(debug=True)
