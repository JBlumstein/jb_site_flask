from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import os, sys

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts/hello')
def render_post():
    return render_template('hello.html')

@app.route('/post_names')
def get_post_names():
	path = "C:/Users/IBM_ADMIN/Documents/flaskapp/templates/posts/"
	dirs = os.listdir( path )
	first_dir = dirs[0]
	return first_dir