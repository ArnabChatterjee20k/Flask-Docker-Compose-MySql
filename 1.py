from flask import Flask
app= Flask("2")
@app.route("/")##end point
def hello():
    return "Hello 1st end ppoint"

@app.route("/1st")##end point
def hello1():
    return "Hello 2nd end ppoint"

app.run(debug=True)
print(type(app))