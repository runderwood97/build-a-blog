from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True 

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:iscmgoe8@localhost:3306/BlogSite'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    text = db.Column(db.String(100))

    def __init__(self, title, text):
        self.title = title
        self.text = text

errorTitle = ""
errorPost = ""

def blogList():
    return [blog for blog in Blog.query.all()]

@app.route("/", methods = ['POST'])
def validatePost():
    postTitle = request.form["postTitle"]
    newBlog = request.form["newBlog"]
    errorCount = 0

    # check to see if the blog title or post are empty
    # if not empty add to database
    # if they are empty increment errorCount and create error discription
    if postTitle != "" and newBlog != "":
        newTitleEscaped = cgi.escape(postTitle, quote = True)
        newBlogEscaped = cgi.escape(newBlog, quote = True)
        
        newPost = Blog(newTitleEscaped, newBlogEscaped)

        db.session.add(newPost)
        db.session.commit()
    else:
        if postTitle == "":
            errorTitle = "Please fill in the title."
            errorCount = errorCount + 1
        if newBlog == "":
            errorPost = "Please fill in the body."
            errorCount = errorCount + 1

    # if an error was created return user to newPost.html with errors listed
    # if no errors created send user user to blog.html with all posts
    if errorCount > 0:
        return render_template('newPost.html', errorTitle = errorTitle, errorPost = errorPost)
    else:
        # loads blog.html and passes in all blogs
        return render_template('blog.html', blogList = blogList())

@app.route("/")
def index():
    # load up newPost.html 
    return render_template('newPost.html', errorTitle = errorTitle, errorPost = errorPost)

if __name__ == "__main__":
    app.run()