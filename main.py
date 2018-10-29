from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True 

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flicklist:MyNewPass@localhost:3306/flicklist'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    blog = db.Column(db.String(100))

    def __init__(self, title, blog):
        self.title = title
        self.blog = blog

@app.route("/", methods = ['post'])
def validatePost():
    postTitle = request.form["postTitle"]
    newBlog = request.form["newBlog"]
    errorCount = 0
    errorTitle = ""
    errorPost = ""

    if postTitle != "" and newBlog != "":
        newTitleEscaped = cgi.escape(postTitle, quote = True)
        newTitle = Blog(newTitleEscaped)

        newBlogEscaped = cgi.escape(newBlog, quote = True)
        newPost = Blog(newBlogEscaped)

        db.session.add(newTitle)
        db.session.add(newPost)
        db.session.commit()

    else:
        if blogTitle = "":
            errorTitle = "Please fill in the title."
            errorCount = errorCount + 1
        if blogText = "":
            errorPost = "Please fill in the body."
            errorCount = errorCount + 1

    if errorCount > 0:
        return render_template('newPost.html', titleError = errorTitle, blogError = errorPost)
    else:
        return render_template('blog.html', )

@app.route("/")
def index():
    return render_template("newPost.html")

app.run()

