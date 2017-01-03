from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import os, sys
import re
from datetime import datetime

app = Flask(__name__)


### posts not to index in list of blog posts
not_blog_posts = set(['index.html', 'base.html', 'hello.html', 'old-website-build.html', 'blog-post-template.html'])


### start functions for displaying blog post information ###

def top_level(folder):
	'''top level function to run on load'''
	jonahs_blog_posts = get_post_names(folder)
	posts_data = []
	for jonahs_blog_post in jonahs_blog_posts:
		if jonahs_blog_post not in not_blog_posts:
			try:
				one_post_data = get_post_data(folder, jonahs_blog_post)
				posts_data.append(one_post_data)
			except:
				continue
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
	description = get_article_description(printed_article)
	post_data = {'post':post, 'stub':stub, 'url_path':url_path, 'title': title, 'date': date, 'description': description}
	return post_data

def print_article(folder, article):
	'''Print out article's jinja template as a string'''
	full_article_path = folder + article
	with open(full_article_path, 'r') as myfile:
		printed_article=myfile.read()
		return printed_article

def get_article_title(article_printout):
	'''get article title from article as string'''
	try:
		article_title = re.findall(r'\{% block title %}(.+?)\{% endblock %}.*?',article_printout)[0]
	except:
		article_title = ""
	return article_title

def get_article_date(article_printout):
	'''get article date from article as string'''
	try:
		article_date = re.findall(r'\<h2 id="date">(.+?)\</h2>.*?',article_printout)[0]
	except:
		article_date = "2015-01-01"
	return article_date	

def get_article_description(article_printout):
	'''get article description from article as string'''
	try:
		article_description = re.findall(r'\{% block description %}(.+?)\{% endblock %}.*?',article_printout)[0]
	except:
		article_description = ""
	return article_description

### end functions for displaying blog post information ###


### run the functions for displaying blog post information ###
### for local on PC###
#blog_posts_and_paths = top_level("C:/Users/IBM_ADMIN/Documents/flaskapp/templates/")
### for local on mac###
#blog_posts_and_paths = top_level("/Users/jonahblumstein/Documents/flaskapp")
### for staging ###
blog_posts_and_paths = top_level("/app/templates/")

### routing ###

@app.route('/')
def index():
	'''render template for index page'''
	return render_template('index.html', blog_posts=blog_posts_and_paths)

@app.route("/blog/<string:blog_post_short_name>/")
def render_one_post(blog_post_short_name):
	'''render blog posts'''
	if blog_post_short_name + '.html' not in not_blog_posts:
		return render_template('%s.html' % blog_post_short_name)