#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import gtk.gdk
import gtk.glade
import gobject
import os.path
from WikiDB import WikiDB

class WikiWidgets:
	def __init__(self,file):
		self.widgets = gtk.glade.XML(file)
	def __getitem__(self,key):
		return self.widgets.get_widget(key)

class WikiWindow:
	def __init__(self):
		if (os.path.exists("../data/wikineitor.glade")):
			glade_file = "../data/wikineitor.glade"

		self.widgets = WikiWidgets(glade_file)
		self.wdb = WikiDB("../wikipedia.db")
	
	def main(self):
		win = self.widgets["wiki-window"]
		win.connect("delete_event", gtk.main_quit)

		#
		# Add completion for search entry
		#
		entry = self.widgets["search-box"]
		completion = gtk.EntryCompletion()
		liststore = gtk.ListStore(gobject.TYPE_STRING)
		completion.set_model(liststore)
		entry.set_completion(completion)
		completion.set_text_column(0)
		for s in self.wdb.get_completion(""):
			liststore.append([s[0]])

		connections = { 
			'search-box/activate'  : self.do_search,
			'search-button/clicked' : self.do_search
		}
		for wid_con, func in connections.iteritems():
			wid,con = wid_con.split('/')
			self.widgets[wid].connect(con,func)

		win.show_all()
		gtk.main()
	
	def do_search(self, button):
		entry = self.widgets['search-box']
		title = entry.get_text()
		(title, page) = self.wdb.get_page(title)
		self.widgets['page-content'].get_buffer().set_text(page)
