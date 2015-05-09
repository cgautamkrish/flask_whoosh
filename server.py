# Gautam Krishnan
# This a purely a hobby project. Hopefully, someone finds this helpful!

from flask import Flask
from flask import render_template
from flask import jsonify
from flask import Flask, render_template, request, url_for

from whoosh.fields import Schema, TEXT, STORED
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
from whoosh.query import *

import threading
import datetime
import time
import sys
import os
import urllib2
import csv
import os.path
reload(sys)
sys.setdefaultencoding("utf-8")
import codecs
from bs4 import BeautifulSoup

import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# instantiating schema
schema = Schema(doc_id=STORED, body=TEXT(stored=True))

# get latest document ID
with open('global.txt') as f:
	global_var = f.read().splitlines()

global_rss_feeds = [
	'rss1.feed.com',
	'rss2.feed.com',
	'rss3.feed.com',
	]

# before server starts, get data and index 
def run_server():
	scrape()
	index()
	app.run()

@app.route("/index", methods=['GET'])
def index():
	path = 'data/'
	num_files = len([f for f in os.listdir(path)	if os.path.isfile(os.path.join(path, f))])
	# creating the index
	if not os.path.exists("index"):
		os.mkdir("index")
		
	ix = create_in("index", schema)
	ix = open_dir("index")
	writer = ix.writer()

	# open the files we had written earlier
	for x in range (1,num_files):
		with open("data/%s" % x , 'r') as content_file:
			content = content_file.read()
			writer.add_document(doc_id=x, body=content.decode('utf-8'))
	print 'Indexing complete..'
	writer.commit()
	return 'ok'

@app.route("/search/<term>")
def searchTerm(term):
	ix = open_dir("index")
	with ix.searcher() as searcher:
		query = QueryParser("body", ix.schema).parse(term)
		results = searcher.search(query)
		# create dictionary to store search results. Eg. 'document_id' : 'document_body'
		search_results = {}
		for result in results:
			print result['doc_id']
			search_results[result['doc_id']] = result['body']
		resp = jsonify(search_results)
		resp.status_code = 200
		return resp

@app.route("/scrape", methods=['GET'])
def scrape():
	path = 'data/'
	num_files = len([f for f in os.listdir(path)	if os.path.isfile(os.path.join(path, f))])

	# url for rss feed
	contenturl = "*******************************"
	hdr = {'User-Agent' : 'Mozilla/5.0'}
	req = urllib2.Request(contenturl, headers=hdr)
	page = urllib2.urlopen(req)
	soup = BeautifulSoup(page.read())

	table = soup.findAll('item')
	doc_id = int(global_var[0])
	for item in table:
		doc_id += 1
		msg_attrs = dict(item.attrs)
		# parse rss feed (xml) and extract
		title = item.find('title').text
		datetime = item.find('pubdate').text
		description = item.find('description').text
		# write to new document
		r = open("data/"+str(doc_id), 'w')
		r.write(title)
		r.write(datetime)
		r.write(description.split('<div', 1)[0])
		r.close()

	# write last file name to global.txt
	global_var_write = open('global.txt', 'w')
	global_var_write.write(str(doc_id))
	global_var_write.close()

	return 'ok'

if __name__ == "__main__":
	handler = RotatingFileHandler('error_log.log', maxBytes=10000, backupCount=1)
	handler.setLevel(logging.INFO)
	app.logger.addHandler(handler)
	run_server()