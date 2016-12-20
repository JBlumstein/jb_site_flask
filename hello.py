from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import os, sys

app = Flask(__name__)

def get_post_names(path):
	dirs = os.listdir( path )
	return dirs

@app.route('/')
def index():
	blog_posts = get_post_names("C:/Users/IBM_ADMIN/Documents/flaskapp/templates/posts/")
	return render_template('index.html', blog_posts=blog_posts)

@app.route('/posts/hello')
def render_post():
	return render_template('hello.html')