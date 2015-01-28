#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Exercise:
# I must:
# 1. Make a window (with Tk or Qt), wich contain next widgets:
#		1) text-field for input text of "reminder me"
#		2) data-time field for enter data of reminder
#		3) button 'Save' - for save information to database
#		4) button 'Show all for today', 'show all for week', 'show all for month' - wich criate new windows with texts about reminders
# 2. Create database (SQLite or PostgreSQL) in existing dir with first start of programm and create all tab in it for saving data.
# 3. Made a controll of row data-time in tab and compare it with today date. If some of that are equal - then show bright window with remindet automaticaly

import sqlite3
from Tkinter import *
import sys
#import os
import datetime

def create_db():
	'''Function create database Sqlite with name: 'reminders.db'  if it's absent in dirrectory with this program
	'''
	# TODO: 1. id must be automaticaly
	try:
		con = sqlite3.connect('reminders.db')
		cur = con.cursor()
		cur.execute('''CREATE TABLE reminders
	 		(id INTEGER PRIMARY KEY autoincrement,
	 		 textReminder VARCHAR(200) not null ,
	 		 date_year INTEGER default 'UNKNOWN',
	 		 date_month INTEGER, 
	 		 date_day INTEGER, 
	 		 date_hour INTEGER, 
	 		 date_minute INTEGER,
				unique (textReminder))''')
		con.commit()
		print 'Create db had done'
		con.close()
	except sqlite3.OperationalError:
		print 'reminders.db had made before'

def reminder_from_cl(len_args):
	print len_args, 'i am hire'
	if len_args == 2:
		print len_args, 'i am hire'
		new_reminder(text = sys.argv[1])
	else:
		try:
			new_reminder(text = sys.argv[1], year = sys.argv[2], month = sys.argv[3], day = sys.argv[4], hour = sys.argv[5], minutes = sys.argv[6])
		except IndexError:
			print 'You must input 6 arguments for entering with comand line!'	

def new_reminder(text = 'New Year', year = datetime.date.today().year, month = datetime.date.today().month, day = datetime.date.today().day, hour = datetime.datetime.now().hour + 1, minutes = datetime.datetime.now().minute):
	'''Function control text of new reminder: if text not new - write it in new message in window,
		if new reminder - write it to database (other fields must be full with information, defaults values are currant time + 1 hour )
		TODO: 1.Use timedelta for writing data in db
	'''
	a = 'INSERT INTO reminders VALUES(null,\"' + str(text) +'", ' +  str(year) +', '+ str(month) +', ' + str(day) + ', ' + str(hour) + ', ' + str(minutes)+ ')'#' + str(id) + ', "'
	print a
	con = sqlite3.connect('reminders.db')
	cur = con.cursor()
	try:
		cur.execute(a)
		con.commit()
	except sqlite3.IntegrityError:
		print 'This value has been entered into database before!'
	con.close()	

def find_actual_rem():
	'''Function control time-fields in all tables and find actualy reminders for currant day
		This Function must be started with set into deltatime
	'''
	# TODO: 1. Use datetime for search
	con = sqlite3.connect('reminders.db')
	cur = con.cursor()
	cur.execute('SELECT *FROM reminders')
	data = cur.fetchall()
	con.close()
	return data

def show_rem():
	'''Function recieves all actualy reminders for today and show all of them in special bright windows
	'''
	pass



#### Main window ####
print sqlite3.version # currant version sqlite3
create_db()

# You can input your reminder in command line with format (after filename must be 6 arguments!):
# ...$ python rem_me.py 'MESSAGE' YEAR MONTH DAY HOUR MIN
if len(sys.argv)>1: reminder_from_cl(len(sys.argv))
	#print len(sys.argv), sys.argv
	

rem_month = []
rem_cur_year = find_actual_rem()
for i in rem_cur_year:
	if i[2] == 2015 and i[3] == 1:
		rem_month.append(i)
	print rem_month
root = Tk()
root.minsize(height = 300, width = 300) # Min size of main window
tx = Text(root, height = 3, width = 70, bg = 'lightgreen', font = "Verdana 14",	wrap = WORD) # textfield
tx.grid(row = 1, column = 0, sticky='nsew')

root.mainloop()