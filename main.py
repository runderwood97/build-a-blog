from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True 

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://runderwood:iscmgoe8@localhost:3306/BlogSite'
app.config['SQLALCHEMY_ECHO'] = True

BlogSite = SQLAlchemy(app)

class Blog(BlogSite.Model):
    id = BlogSite.Column(BlogSite.Integer, primary_key=True)
    title = BlogSite.Column(BlogSite.String(40))
    text = BlogSite.Column(BlogSite.String(100))

    def __init__(self, title, text):
        self.title = title
        self.text = text

errorTitle = ""
errorPost = ""

def blogList():
    return Blog.query.all()

@app.route("/", methods = ['post'])
def validatePost():
    postTitle = request.form["postTitle"]
    newBlog = request.form["newBlog"]
    errorCount = 0

    # check to see if the blog title or post are empty
    # if not empty add to database
    # if they are empty increment errorCount and create error discription
    if postTitle != "" and newBlog != "":
        newTitleEscaped = cgi.escape(postTitle, quote = True)
        newTitle = Blog(newTitleEscaped)

        newBlogEscaped = cgi.escape(newBlog, quote = True)
        newPost = Blog(newBlogEscaped)

        BlogSite.session.add(newTitle)
        BlogSite.session.add(newPost)
        BlogSite.session.commit()
    else:
        if blogTitle == "":
            errorTitle = "Please fill in the title."
            errorCount = errorCount + 1
        if blogText == "":
            errorPost = "Please fill in the body."
            errorCount = errorCount + 1

    # if an error was created return user to newPost.html with errors listed
    # if no errors created send user user to blog.html with all posts
    if errorCount > 0:
        return render_template('newPost.html', titleError = errorTitle, blogError = errorPost)
    else:
        # loads blog.html and passes in all blogs
        return render_template('blog.html', blogList = blogList)

@app.route("/")
def index():
    # load up newPost.html 
    return render_template('base.html', errorTitle = errorTitle, errorPost = errorPost)

app.run()

