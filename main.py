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
    text = db.Column(db.String(100))

    def __init__(self, title, text):
        self.title = title
        self.text = text

def getBlogTitles():
    # gathers all blog titles
    return [title for title in Blog.query.all()]

def getBlogText():
    # gathers all blog texts
    return [text for text in Blog.query.all()]

@app.route("/", methods = ['post'])
def validatePost():
    postTitle = request.form["postTitle"]
    newBlog = request.form["newBlog"]
    errorCount = 0
    errorTitle = ""
    errorPost = ""

    # check to see if the blog title or post are empty
    # if not empty add to database
    # if they are empty increment errorCount and create error discription
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

    # if an error was created return user to newPost.html with errors listed
    # if no errors created send user user to blog.html with all posts
    if errorCount > 0:
        return render_template('newPost.html', titleError = errorTitle, blogError = errorPost)
    else:
        return render_template('blog.html', titleList = newTitle, textList = newPost)

@app.route("/")
def index():
    # load up newPost.html 
    return render_template("newPost.html")

app.run()

