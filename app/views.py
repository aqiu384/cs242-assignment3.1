from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db
from forms import PostForm
from models import Post
from datetime import datetime
from SvnParser import SvnParser
import re

#Stores tuples of censored words and their corresponding allowable ones
replacement_str = [('fuck', 'fornicate'), ('damn', 'darn'), ('ass', 'anus'), ('bastard', 'John Snow'), ('goto', 'he-who-must-not-be-named')]

#Load and parse the SVN files into the website
svn_parser = SvnParser('svn_list.xml', 'svn_log.xml')
svn_parser.init_project_list()
svn_parser.init_file_list()
svn_parser.init_revision_list()

def filter_words(str):
    """Filters out censored words and replaces them with nice ones in a string"""
    for pair in replacement_str:
        replacer = re.compile(re.escape(pair[0]), re.IGNORECASE)
        str = replacer.sub(pair[1], str)
    return str

def build_tree(id):
    """Recursively queries database and builds a tree of nested comments in chronological order"""
    return [(row, build_tree(row.id)) for row in db.session.query(Post).filter_by(pid = id).\
        order_by(Post.timestamp)]

@app.route('/')
@app.route('/index')
def index():
    """Index page with listings of projects and comments"""
    projects = svn_parser.projects
    files = svn_parser.files
    
    post_tree = build_tree(0)
    
    return render_template("index.html",
        title = 'Home',
        projects = projects,
        files = files,
        post_tree = post_tree)

@app.route('/respond/<pid>', methods = ['GET', 'POST'])
def respond_post(pid):
    """Reponse redirect page for adding a new comment"""
    form = PostForm()
    
    if form.validate_on_submit():
        post = Post(body = filter_words(form.body.data), 
                    timestamp = datetime.utcnow(), 
                    author = filter_words(form.author.data), 
                    pid = pid)
                    
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
        
    return render_template('respond.html',
        title = 'Response Page',
        form = form)
        
@app.route('/project/<project>')
def project_page(project):
    """Project page featuring list of files in that project"""
    files = svn_parser.files[project]
    return render_template("project_page.html",
        title = 'Project Page',
        project = project,
        files = files)
        
@app.route('/revision/<path:file>')
def revision_page(file):
    """Revision page featuring the revisions and source of a particular file"""
    revisions = svn_parser.revisions[file]
    return render_template("revision_page.html",
        title = 'Revision Page',
        file = file,
        revisions = revisions)