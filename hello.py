from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import os, sys
import re

app = Flask(__name__)

def top_level(folder):
	'''top level function to run on load'''
	jonahs_blog_posts = get_post_names(folder)
	posts_data = []
	for jonahs_blog_post in jonahs_blog_posts:
		one_post_data = get_post_data(folder, jonahs_blog_post)
		posts_data.append(one_post_data)
	for single_post in posts_data:
		route_one_post(single_post)
	return posts_data

def get_post_names(path):
	'''get a list of posts from a folder'''
	dirs = os.listdir( path )
	return dirs

def get_post_data(folder, post):
	'''get post data from each post'''
	stub = post[:-5]
	url_path = '/posts/' + stub
	printed_article = print_article(folder, post)
	blog_title = get_article_title(printed_article)
	blog_date = get_article_date(printed_article)
	post_data = {'post':post, 'stub':stub, 'url_path':url_path, 'blog_title': blog_title, 'blog_date': blog_date}
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
	article_date = re.findall(r'\{% block date %}(.+?)\{% endblock %}.*?',article_printout)[0]
	return article_date	

def route_one_post(item):
	'''create the routing for a single post'''
	one_post_path = item['url_path']
	@app.route(one_post_path)
	def render_one_post():
		return render_template(item['post'])

blog_posts_and_paths = top_level("C:/Users/IBM_ADMIN/Documents/flaskapp/templates/posts/")

@app.route('/')
def index():
	'''render template for index page'''
	return render_template('index.html', blog_posts=blog_posts_and_paths)

@app.route('/resume')
def load_resume():
	'''render template for index page'''
	return render_template('resume.html')