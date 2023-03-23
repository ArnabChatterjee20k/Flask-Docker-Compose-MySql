## static - for  public
## templates - private  folder

from flask import Flask,render_template
app=Flask("2")
@app.route("/")
def hello():
    return render_template("index.html")
@app.route("/1st")
def hello1():
    name="Arnab"
    return render_template("index2.html",myname=name)## maname is used in index2
app.run(debug=True)