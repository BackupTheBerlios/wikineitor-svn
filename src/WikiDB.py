#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite

class WikiDB:
	def __init__(self, file):
		self.conn = sqlite.connect(file, encoding="utf-8")
	
	def get_completion(self, start_text):
		cur = self.conn.cursor()
		cur.execute("SELECT cur_title FROM cur WHERE cur_title LIKE '%s%%'" % start_text)
		return cur.fetchall()
	
	def page_exists(self, page_title):
		cur = self.conn.cursor()
		cur.execute("SELECT cur_title FROM cur WHERE cur_title = '%s'" % page_title)
		return (cur.fetchone() != None)
	
	def get_page(self, page_title):
		cur = self.conn.cursor()
		cur.execute("SELECT cur_title, cur_text FROM cur WHERE cur_title = '%s'" % page_title)
		return cur.fetchone()

