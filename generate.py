#!/usr/bin/python
"""
Generates a blog entry from input data.
Requires: 
python-slugify (pip install python-slugify)
pystache (pip install pystache)
markdown (pip install markdown)
"""
import argparse
import json
from slugify import slugify
import re
import os
import pystache
import markdown
import time

def get_config(f):
	config = json.loads(open(args.configfile, 'r').read())

	if not 'slug' in config:
		config['slug'] = slugify(config['title'])

	if not 'source' in config:
		basename = re.search('content/(.+).json', args.configfile).group(1)
		md = 'content/%s.md' % basename
		html = 'content/%s.html' % basename
	
		if os.path.exists(md):
			config['source'] = md
		else:
			config['source'] = html
	elif not re.match('content/', config['source']):
		config['source'] = 'content/'+config['source']

	d = time.strptime(config['date'], '%Y-%m-%d %H:%M')
	config['date_published'] = time.strftime('%A, %d-%m-%Y', d)
	
	return config

parser = argparse.ArgumentParser(description='Generate blog entry')
parser.add_argument('configfile', metavar='config-file')
parser.add_argument('--next', help='Config file for the next blog entry', dest='next')
parser.add_argument('--previous', help='Config file for the previous blog entry', dest='prev')
parser.add_argument('--latest', help='Config files for the latest blog entries', nargs='+', dest='latest')

args = parser.parse_args()
config = get_config(args.configfile)

source = open(config['source'], 'r').read()
if re.search('\.md$', config['source']):
	source = markdown.markdown(source)

page = open('post.mustache', 'r').read()
config['content'] = source

if args.next:
	cfg = get_config(args.next)
	config['next'] = {
		'link': cfg['slug']+'.html',
		'title': cfg['title']
	}

if args.prev:
	cfg = get_config(args.prev)
	config['previous'] = {
		'link': cfg['slug']+'.html',
		'title': cfg['title']
	}

if args.latest:
	latest = []
	for post in args.latest:
		cfg = get_config(post)
		latest.append({'link': cfg['slug']+'.html', 'title': cfg['title']})

	config['latest'] = latest

print pystache.render(page, config)

