from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, send_from_directory
import os, sys
import re
from datetime import datetime

app = Flask(__name__)


### posts not to index in list of blog posts
not_blog_posts = set(['index.html', 'base.html', 'hello.html', 'old-website-build.html', 'blog-post-template.html', 'index-with-tagged-posts.html', 'main-page-base.html'])


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
	posts_tags = get_tags(posts_data)
	tag_counts = get_tag_counts(posts_tags)
	top_tag_counts = list(tag_count for tag_count in tag_counts if tag_count['tag_count']>=3)
	top_tag_counts = sorted(top_tag_counts, key=lambda k: k['tag_count'], reverse=True)
	return posts_data, top_tag_counts

def get_post_names(path):
	'''get a list of posts from a folder'''
	dirs = os.listdir( path )
	return dirs

def get_post_data(folder, post):
	'''get post data from each post'''
	stub = post[:-5]
	url_path = '/blog/' + str(stub)
	printed_article = print_article(folder, post)
	title = get_article_attribute(printed_article, 'title', 'Untitled')
	date = get_article_attribute(printed_article, 'date', '2015-01-01')
	date = datetime.strptime(date, '%Y-%m-%d').date()
	description = get_article_attribute(printed_article, 'description', 'No description')
	tags = get_article_attribute(printed_article, 'tags', '')
	tags = tags.split(sep=', ')
	tags = set(tags)
	post_data = {'post':post, 'stub':stub, 'url_path':url_path, 'title': title, 'date': date, 'description': description, 'tags': tags}
	return post_data

def print_article(folder, article):
	'''Print out article's jinja template as a string'''
	full_article_path = folder + article
	with open(full_article_path, 'r') as myfile:
		printed_article=myfile.read()
		return printed_article

def get_article_attribute(article_printout, attribute, fallback):
	'''get article attributes from article as string'''
	search_string = '\{% block ' + attribute + ' %}(.+?)\{% endblock %}.*?'
	try:
		article_attribute = re.findall(search_string, article_printout)[0]
	except:
		article_attribute = fallback
	return article_attribute

def get_tags(all_posts_data):
	'''extract a list of all tags for posts'''
	all_post_tags = []
	for one_post_data in all_posts_data:
		one_post_tags = list(one_post_data['tags'])
		all_post_tags.extend(one_post_tags)
	return all_post_tags

def get_tag_counts(all_tags):
	'''create a dict with each tag and the number of times that tag is used'''
	all_tags_data = []
	unique_tags = set(all_tags)
	for tag in unique_tags:
		tag_data = {'tag_name': tag, 'tag_count': all_tags.count(tag)}
		all_tags_data.append(tag_data)
	return all_tags_data

### end functions for displaying blog post information ###


### run the functions for displaying blog post information ###
### for local on IBM mac###
# blog_posts_and_paths, tags_and_counts = top_level("/Users/jblumst@us.ibm.com/Documents/personal_website/jb_site_flask/templates/")
### for local on personal mac###
blog_posts_and_paths, tags_and_counts = top_level("/Users/jonahblumstein/Documents/jb_site_flask/")
### for staging ###
# blog_posts_and_paths, tags_and_counts = top_level("/app/templates/")

### routing ###

@app.route('/')
def index():
	'''render template for index page'''
	return render_template('index.html', blog_posts=blog_posts_and_paths, tags_and_counts=tags_and_counts)

@app.route("/etc/<path:filename>")
def download_file(filename):
    return send_from_directory('html_static', filename)

@app.route("/blog/<string:blog_post_short_name>/")
def render_one_post(blog_post_short_name):
	'''render blog posts'''
	if blog_post_short_name + '.html' not in not_blog_posts:
		single_post_tags = list(item['tags'] for item in blog_posts_and_paths if item['stub'] == blog_post_short_name)[0]
		return render_template('%s.html' % blog_post_short_name, single_post_tags=single_post_tags)

@app.route("/blog_posts_tagged:<string:tag>/")
def render_list_of_tagged_posts(tag):
	'''render index page with posts with desired tag'''
	return render_template('index-with-tagged-posts.html', blog_posts=blog_posts_and_paths, tag=tag)

@app.route('/video2minutes')
def video2minutes():
	return redirect("https://www.youtube.com/watch?v=yuoW5wFU2Ks")

@app.route('/video15minutes')
def video15minutes():
	return redirect("https://youtu.be/aiwFm6MiPqY")