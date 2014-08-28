# -*- coding: utf-8 -*-
#!/usr/bin/env python

import argparse
import sys
import json
import os.path
import datetime

from imdbpie import Imdb
from prettytable import *
from jinja2 import Template

jsonFileName = "top.json"
asciiFileName = "index.txt"
htmlFileName = "index.html"
htmlTemplateName = "top_template.html"

def create_argument_parser():
	parser = argparse.ArgumentParser(
		description = "Find the newly added movies to imdb's top 250." )

	parser.add_argument('-f', '--fetch', action='store_true', required=False, help="fetch imdb's current top 250 list")
	parser.add_argument('-a', '--ascii', action='store_true', required=False, help="print the newly added items in ascii format")
	parser.add_argument('-w', '--html', action='store_true', required=False, help="print the newly added items in html format")
	parser.add_argument('-b', '--both', action='store_true', required=False, help="print both the ascii and the html formats")

	return parser

def fetch_top250():
	imdb = Imdb()

	top = imdb.top_250()

	return top

def fetch_data():
	today = datetime.datetime.now()

	ret = {
		"top" : None,
		"info" : {
			"date" : today.ctime()
		}
	}

	top = fetch_top250()
	ret["top"] = top

	return ret

def write_top_to_file(json):
	f = open(jsonFileName, 'w')
	f.write(json)
	f.close()

def get_top250():
	if not os.path.isfile(jsonFileName):
		top = fetch_data()
		write_top_to_file(json.dumps(top))

	f = open(jsonFileName, 'r')
	jsonTop = f.read()
	f.close()

	return json.loads(jsonTop)

def search_top(id, dicts):
	return next((item for item in dicts if item["tconst"] == id), None)

def print_ascii(newlyAdded, data, date):
	if len(newlyAdded) == 0:
		ret = "Last check: %s\n\n" % date
		ret = ret + "No new entries"

		return ret

	newTop = data["top"]
	newlyAddedDicts = [search_top(itemId, newTop) for itemId in newlyAdded]

	table = PrettyTable()
	fieldNames = ["Title", "Rating", "Votes", "URL"]
	table.field_names = fieldNames
	table.align = "l"

	for movie in newlyAddedDicts:
		url = "http://www.imdb.com/title/%s/" % (movie["tconst"])
		table.add_row([movie["title"], movie["rating"], movie["num_votes"], url])

	ret = "Last check: %s\n\n" % date
	ret = ret + table.get_string(sortby="Rating", reversesort=True)

	return ret

def read_html_template():
	f = open(htmlTemplateName, 'r')
	html = f.read()
	f.close()

	return html

def print_html(newlyAdded, data, date):
	newTop = data["top"]
	newlyAddedDicts = [search_top(itemId, newTop) for itemId in newlyAdded]

	htmlTemplate = read_html_template()
	template = Template(htmlTemplate)

	return template.render(movies=newlyAddedDicts, date=date)

def write_ascii(text):
	f = open(asciiFileName, 'w')
	f.write(text)
	f.close()

def write_html(text):
	f = open(htmlFileName, 'w')
	f.write(text)
	f.close()

if __name__ == "__main__":
	argParser = create_argument_parser()
	argsList = sys.argv

	del argsList[0]

	args = argParser.parse_args(argsList)

	data = fetch_data()
	newTop = data["top"]

	if args.fetch:
		write_top_to_file(json.dumps(data))

	fileData = get_top250()
	top = fileData["top"]

	newTopList = [item["tconst"] for item in newTop]
	topList = [item["tconst"] for item in top]

	newlyAdded = set(newTopList) - set(topList)

	if args.ascii:
		write_ascii(print_ascii(newlyAdded, data, fileData["info"]["date"]))

	if args.html:
		write_html(print_html(newlyAdded, data, fileData["info"]["date"]))

	if args.both:
		write_ascii(print_ascii(newlyAdded, data, fileData["info"]["date"]))
		write_html(print_html(newlyAdded, data, fileData["info"]["date"]))

	print "Done"
	sys.exit(0)
