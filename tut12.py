from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy,request
from flask_mail import Mail
from datetime import datetime
import json

with open("config.json")as c:
    params=json.load(c)["params"]

local_server=True
app=Flask("2")
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-password']
)
mail=Mail(app)
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
else:
    app.config['SQLALCHEMY_DATABASE_URI']=params["prod_uri"]
db=SQLAlchemy(app)
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     email = db.Column(db.String(120), unique=True)

class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12),unique=True, nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20),unique=True,nullable=False)

class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(25), nullable=False)
    content= db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    title=db.Column(db.String(20),nullable=False)
    subtitle = db.Column(db.String(20), nullable=False)

@app.route("/")
def home():
    return render_template("index.html",params=params)

@app.route("/about")
def about():
    return render_template("about.html",params=params)

@app.route("/post/<string:post_slug>",methods=['GET'])
def post_route(post_slug):
    post=Posts.query.filter_by(slug=post_slug).first() ## fetching the data by slug
    posted_by = Contact.query.get(2)### fetching by primary key
    # posted_by=Contact.query.get(post.sno)## fetching by post_slug sno and using that sno in contacts
    return render_template('post.html',params=params,post=post,posted_by=posted_by) ## tile of  the data fetched by slug as it is unique

@app.route("/contact",methods=["GET","POST"])
def contact():
    if request.method=="POST":
        name=request.form.get("name")
        phone=request.form.get("phn")
        email=request.form.get("email")
        message=request.form.get("message")
        entry=Contact(name=name,phone_num=phone,msg=message,date=datetime.now(),email=email)
        db.session.add(entry)
        db.session.commit()
        mail.send_message(
            f"Msg from{name}",
            sender=email,
            recipients=[params["gmail-user"]],
            body = f"{message}\n{phone}"
        )
    return render_template("contact.html",params=params)

@app.route("/post")
def post():
    return render_template("post.html",params=params)
app.run(debug=True)