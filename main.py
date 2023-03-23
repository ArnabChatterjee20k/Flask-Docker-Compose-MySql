from flask import Flask,render_template,session,redirect,request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import datetime
import json,os
from werkzeug.utils import secure_filename

with open("config.json")as c:
    params=json.load(c)["params"]

local_server=True
app=Flask(__name__)
app.config["UPLOAD_FOLDER"]=params["upload_location"]
app.secret_key="Super-secret_key"
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
    img_file=db.Column(db.String(20),nullable=False)
    subtitle = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    posts = Posts.query.filter_by().all()[0:int(params["no_of_post"])]
    return render_template("index.html",params=params,posts=posts)

@app.route("/dashboard",methods=["GET","POST"])
def dashboard():
    if "user" in session and session['user']==params['admin_user']:###to check user is loged in or not
        post=Posts.query.all()
        return render_template("dashboard.html", params=params,posts=post)
    if request.method=="POST":
        username=request.form.get("uname")
        userpass=request.form.get("upass")
        if username==params["admin_user"] and userpass==params["admin_password"]:
            session["user"]=username
            post = Posts.query.all()
            return render_template("dashboard.html",params=params,posts=post)

    return render_template("login.html", params=params)

@app.route("/edit/<string:sno>",methods=["GET","POST"])
def edit(sno):
    if "user"in session and session["user"]==params["admin_user"]:
        if request.method=="POST":
            box_title=request.form.get("title")
            sub=request.form.get("subtitle")
            slug=request.form.get("slug")
            content=request.form.get("content")
            img=request.form.get("img")
            date=datetime.now()
        # if sno is 0 then we will adding post and if sno is not 0 then we will be editimg it.
            if sno=="0":
                post=Posts(title=box_title,subtitle=sub,slug=slug,content=content,date=date,img_file=img)
                db.session.add(post)
                db.session.commit()
            else:
                post=Posts.query.filter_by(sno=sno).first()
                post.title=box_title
                post.subtitle=sub
                post.slug=slug
                post.content=content
                post.img_file=img
                db.session.commit()
                return redirect(f"/edit/{sno}")
        post=Posts.query.filter_by(sno=sno).first()
        return render_template("edit.html",params=params,post=post)

@app.route("/uploader",methods=["GET","POST"])
def upload():
    if "user" in session and session['user']==params['admin_user']:
            if request.method=="POST":
                f=request.files["file1"]
                f.save(os.path.join(app.config["UPLOAD_FOLDER"],secure_filename(f.filename)))
                return "Uploaded Successfully"
@app.route("/logout")
def logout():
    session.pop("user")
    return redirect("/dashboard")

@app.route("/about")
def about():
    return render_template("about.html",params=params)
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
@app.route("/post/<string:post_slug>",methods=['GET'])
def post_route(post_slug):
    post=Posts.query.filter_by(slug=post_slug).first() ## fetching the data by slug
    return render_template('post.html',params=params,post=post) ## tile of  the data fetched by slug as it is unique

app.run(debug=True)