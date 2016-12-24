from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import os, sys
import re
from datetime import datetime

app = Flask(__name__)

not_blog_posts = set(['index.html', 'base.html'])

def top_level(folder):
	'''top level function to run on load'''
	jonahs_blog_posts = get_post_names(folder)
	posts_data = []
	for jonahs_blog_post in jonahs_blog_posts:
		if jonahs_blog_post not in not_blog_posts:
			one_post_data = get_post_data(folder, jonahs_blog_post)
			posts_data.append(one_post_data)
	posts_data = sorted(posts_data, key=lambda k: k['date'], reverse=True) 
	return posts_data

def get_post_names(path):
	'''get a list of posts from a folder'''
	dirs = os.listdir( path )
	return dirs

def get_post_data(folder, post):
	'''get post data from each post'''
	stub = post[:-5]
	url_path = '/blog/' + str(stub)
	printed_article = print_article(folder, post)
	title = get_article_title(printed_article)
	date = get_article_date(printed_article)
	date = datetime.strptime(date, '%Y-%m-%d').date()
	post_data = {'post':post, 'stub':stub, 'url_path':url_path, 'title': title, 'date': date}
	return post_data

def print_article(folder, article):
	'''Print out article'''
	full_article_path = folder + article
	with open(full_article_path, 'r') as myfile:
		printed_article=myfile.read()
		return printed_article

def get_article_title(article_printout):
	'''get article title from article as string'''
	article_title = re.findall(r'\{% block title %}(.+?)\{% endblock %}.*?',article_printout)[0]
	return article_title

def get_article_date(article_printout):
	'''get article date from article as string'''
	article_date = re.findall(r'\<h2 id="date">(.+?)\</h2>.*?',article_printout)[0]
	return article_date	

blog_posts_and_paths = top_level("C:/Users/IBM_ADMIN/Documents/flaskapp/templates/")

@app.route('/')
def index():
	'''render template for index page'''
	return render_template('index.html', blog_posts=blog_posts_and_paths)

@app.route('/resume')
def load_resume():
	'''render template for index page'''
	return render_template('resume.html')

@app.route("/blog/<string:blog_post_short_name>/")
def render_one_post(blog_post_short_name):
	'''render blog posts'''
	if blog_post_short_name + '.html' not in not_blog_posts:
		return render_template('%s.html' % blog_post_short_name)