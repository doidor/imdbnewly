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

class ImdbNewly:
	_imdb = None
	_newTop = None
	_oldTop = None
	_newlyAdded = None
	_storedTopFile = "top.json"

	def __init__(self):
		self._imdb = Imdb()
		self._oldTop = self._get_stored_data()
		self._oldTopList = self._generate_oldTop_id_list()
		self._newTop = self._fetch_data()
		self._newTopList = self._generate_newTop_id_list()
		self._newlyAdded = self._find_newly_added()

	def _fetch_data(self):
		today = datetime.datetime.now()

		ret = {
			"top" : self._imdb.top_250(),
			"info" : {
				"date" : today.ctime()
			}
		}

		return ret

	def save_top_data(self):
		top = self._fetch_data()

		f = open(self._storedTopFile, 'w')
		f.write(json.dumps(top))
		f.close()

	def _generate_oldTop_id_list(self):
		return [item["tconst"] for item in self._oldTop["top"]]

	def _generate_newTop_id_list(self):
		return [item["tconst"] for item in self._newTop["top"]]

	def _get_stored_data(self):
		if not os.path.isfile(self._storedTopFile):
			self.save_top_data()

		f = open(self._storedTopFile, 'r')
		jsonTop = f.read()
		f.close()

		return json.loads(jsonTop)

	def _search_newTop_data(self, id):
		return next((item for item in self._newTop["top"] if item["tconst"] == id), None)

	def _find_newly_added(self):
		return set(self._newTopList) - set(self._oldTopList)

	def get_newly_added(self):
		return [self._search_newTop_data(itemId) for itemId in self._newlyAdded]

	def get_newTop_date(self):
		return self._newTop["info"]["date"]

	def get_oldTop_date(self):
		return self._oldTop["info"]["date"]

class ImdbNewlyExporter:
	_imdbNewly = None
	_newlyAddedDicts = None
	_oldListDate = None
	_newListDate = None

	_asciiFileName = "index.txt"
	_htmlFileName = "index.html"
	_htmlTemplateName = "top_template.html"

	def __init__(self, imdbNewly):
		self._imdbNewly = imdbNewly

		self._newlyAddedDicts = self._imdbNewly.get_newly_added()
		self._oldListDate = self._imdbNewly.get_oldTop_date()
		self._newListDate = self._imdbNewly.get_newTop_date()

	def _parse_html_template(self):
		f = open(self._htmlTemplateName, 'r')
		html = f.read()
		f.close()

		return html

	def _get_ascii(self):
		if len(self._newlyAddedDicts) == 0:
			ret = "Top 250 list date: %s\n" % self._oldListDate
			ret = ret + "Last check date: %s\n\n" % self._newListDate
			ret = ret + "No new entries"

			return ret

		table = PrettyTable()
		table.field_names = ["Title", "Rating", "Votes", "URL"]
		table.align = "l"

		for movie in self._newlyAddedDicts:
			url = "http://www.imdb.com/title/%s/" % (movie["tconst"])
			table.add_row([movie["title"], movie["rating"], movie["num_votes"], url])

		ret = "Top 250 list date: %s\n" % self._oldListDate
		ret = ret + "Last check date: %s\n\n" % self._newListDate
		ret = ret + table.get_string()

		return ret

	def _get_html(self):
		htmlTemplate = self._parse_html_template()
		template = Template(htmlTemplate)

		return template.render(movies=self._newlyAddedDicts, oldListDate=self._oldListDate, newListDate=self._newListDate)

	def _write_to_file(self, fileName, text):
		f = open(fileName, 'w')
		f.write(text)
		f.close()

	def write_export(self, exportType="both"):
		if exportType == "both":
			self._write_to_file(self._htmlFileName, self._get_html())
			self._write_to_file(self._asciiFileName, self._get_ascii())
		elif exportType == "html":
			self._write_to_file(self._htmlFileName, self._get_html())
		elif exportType == "ascii":
			self._write_to_file(self._asciiFileName, self._get_ascii())


def create_argument_parser():
	parser = argparse.ArgumentParser(
		description = "Find the newly added movies to imdb's top 250." )

	parser.add_argument('-f', '--fetch', action='store_true', required=False, help="fetch imdb's current top 250 list")
	parser.add_argument('-a', '--ascii', action='store_true', required=False, help="print the newly added items in ascii format")
	parser.add_argument('-w', '--html', action='store_true', required=False, help="print the newly added items in html format")
	parser.add_argument('-b', '--both', action='store_true', required=False, help="print both the ascii and the html formats")

	return parser

if __name__ == "__main__":
	imdbNewly = ImdbNewly()
	imdbNewlyExporter = ImdbNewlyExporter(imdbNewly)

	argParser = create_argument_parser()
	argsList = sys.argv

	del argsList[0]

	args = argParser.parse_args(argsList)

	if args.fetch:
		print "Refetching data..."
		imdbNewly.save_top_data()

	if args.ascii:
		print "Exporting in ascii mode"
		imdbNewlyExporter.write_export(exportType="ascii")

	if args.html:
		print "Exporting in html mode"
		imdbNewlyExporter.write_export(exportType="html")

	if args.both:
		print "Exporting in both ascii and html modes"
		imdbNewlyExporter.write_export()

	print "Done"
	sys.exit(0)
