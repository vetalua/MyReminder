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

##### Today is ########
day_default = datetime.datetime.now().day
month_default = datetime.datetime.now().month
year_default = datetime.datetime.now().year
hour_default = datetime.datetime.now().hour
minute_default = datetime.datetime.now().minute

def create_db():
	'''Function creates database Sqlite with name: 'reminders.db'  if it's absent in dirrectory with this program
	'''
	# TODO: 1. id must be automaticaly - Done
	#		2. Another fields must be adding (rem for avryyear or no)!
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
		print 'Creating db had done'
		con.close()
	except sqlite3.OperationalError:
		print 'reminders.db had made before'

def reminder_from_cl(len_args):
	'''Function works with values wich had entered from comand line. You can don't use  this method, but use entering with GUI
	'''
	#TODO:	1. Use arguments with names ?!
	if len_args == 2:
		#print len_args, 'i am hire'
		new_reminder(text = sys.argv[1])
	else:
		try:
			new_reminder(text = sys.argv[1], year = sys.argv[2], month = sys.argv[3], day = sys.argv[4], hour = sys.argv[5], minutes = sys.argv[6])
		except IndexError:
			print 'You must input 6 arguments for entering with comand line!'	

def new_reminder(text = 'New Year', year = year_default, month = month_default, day = day_default, hour = hour_default + 1, minutes = minute_default):
	'''Function controls text of new reminder: if text not new - write it in new message in window,
		if new reminder - write it to database (other fields must be full with information, defaults values are current time + 1 hour )
		TODO: 1.Use timedelta for writing data in db
	'''
	require = 'INSERT INTO reminders VALUES(null,\"' + str(text) +'", ' +  str(year) +', '+ str(month) +', ' + str(day) + ', ' + str(hour) + ', ' + str(minutes)+ ')'#' + str(id) + ', "'
	print require
	con = sqlite3.connect('reminders.db')
	cur = con.cursor()
	try:
		cur.execute(require)
		con.commit()
	except sqlite3.IntegrityError:
		print 'This value has been entered into database before!'
	con.close()	

def find_actual_rem( year = year_default, month = month_default, day = day_default):
	'''Function controls date_ fields in all tables and find actualy reminders for current day
		This Function must be started with set into deltatime
	'''
	# TODO: 1. Use datetime for search
	
	require = 'SELECT textReminder, date_hour, date_minute from reminders where date_year = \"' + str(year) +'\" and date_month = \"' + str(month) + '\" and date_day = \"'+ str(day) +'\"'
	#print require
	con = sqlite3.connect('reminders.db')
	cur = con.cursor()
	cur.execute(require) #('SELECT textReminder, date_hour, date_minute from reminders where date_month = "2"')#  <<<--- old
	data = cur.fetchall()
	con.close()
	return data

def show_rem():
	'''Function recieves  actual reminder for this time and show it in special bright windows
	'''
	pass

def save_reminder(event):
	'''Function works when user press to button 'Save' and reads text from the textfield and from the date-fields. 
	If it isn't problem with entered data, call function new_reminder
	'''
	#print 'You call save_reminder function'
	new_reminder(text = unicode(tx.get('1.0', 'end')))
	#print ent_day.get('1.0', 'end')
	#print text


def reminder_today(event):
	'''Function all reminders for today
	'''
	# TODO: 1. Must show reminders in special window with comfort for reading form
	actual_today = find_actual_rem(day = day_default)
	print actual_today # show list of reminders for today in comand last. 

	
def reminder_this_week(event):
	print 'You call reminder_this_week function'
	try:
		day = int(ent_day.get())
	except ValueError:
		ent_day.delete(0, END)
		ent_day.insert(0, day_default)
		print day_ent.get()

	if not(day>0 and day<32):
		ent_day.delete(0, END)
		ent_day.insert(0, day_default)
	print ent_day.get()

def reminder_this_month(event):
	print 'You call reminder_this_month function'



#### Main window ####
print sqlite3.version # currant version sqlite3
create_db()

# You can input your reminder in command line with format (after filename must be 6 arguments!):
# ...$ python rem_me.py 'MESSAGE' YEAR MONTH DAY HOUR MIN
if len(sys.argv)>1: reminder_from_cl(len(sys.argv))
	#print len(sys.argv), sys.argv
	
rem_month = find_actual_rem()
#rem_month = []
#rem_cur_year = find_actual_rem()
#for i in rem_cur_year:
#	if i[2] == 2015 and i[3] == 1:
#		rem_month.append(i)
#	print rem_month
print rem_month

root = Tk()
root.title(' My reminders')
root.minsize(height = 300, width = 300) # Min size of main window

lab = Label(root, text = 'Write your reminder hire:', font = 'Verdana 12')
lab.grid(row = 0, column = 0)

tx = Text(root, height = 6, width = 25, bg = 'lightgreen', font = "Verdana 14",	wrap = WORD) # textfield
tx.grid(row = 1, column = 0, sticky='nsew')

lab = Label(root, text = 'Write date:', font = 'Verdana 12')
lab.grid(row = 0, column = 1)

#fra = Frame(root, height = 80, width = 700, bg = 'green')
#fra.grid(row = 3, column = 0)
lab = Label(root, text = 'Day:', font = 'Verdana 10')
lab.grid(row = 1, column = 1)

ent_day = Entry(root, width = 2, bd = 2)
ent_day.insert(0, day_default)
ent_day.grid(row = 1, column = 2)
ent_day.bind('<Motion>', reminder_today)
#ent_day.pack()

lab = Label(root, text = 'Month:', font = 'Verdana 10')
lab.grid(row = 2, column = 1)

ent_month = Entry(root, width = 2, bd = 2)
ent_month.insert(0, month_default)
ent_month.grid(row = 2, column = 2)

lab = Label(root, text = 'Year:', font = 'Verdana 10')
lab.grid(row = 3, column = 1)

ent_year = Entry(root, width = 4, bd = 2)
ent_year.insert(0, year_default)
ent_year.grid(row = 3, column = 2)

lab = Label(root, text = 'Hour:', font = 'Verdana 10')
lab.grid(row = 4, column = 1)

ent_hour = Entry(root, width = 4, bd = 2)
ent_hour.insert(0, hour_default+1)
ent_hour.grid(row = 4, column = 2)

lab = Label(root, text = 'Minutes:', font = 'Verdana 10')
lab.grid(row = 5, column = 1)

ent_minute = Entry(root, width = 4, bd = 2)
ent_minute.insert(0, minute_default)
ent_minute.grid(row = 5, column = 2)

##### BUTTONS #####
but1 = Button(root, height = 1, width = 20, font = 'Verdana 20', bg = 'gold', activebackground = 'green')
but1['text'] = "Save"
but1.bind('<Button-1>', save_reminder)
but1.grid(row = 2,  column = 0)

but2 = Button(root)
but2['text'] = "Reminders for today"
but2.bind('<Button-1>', reminder_today)
but2.grid(row = 6,  column = 0)

but3 = Button(root)
but3['text'] = "Rem for week"
but3.bind('<Button-1>', reminder_this_week)
but3.grid(row = 6,  column = 1)

but4 = Button(root)
but4['text'] = "Reminders for month"
but4.bind('<Button-1>', find_actual_rem(month = month_default))
but4.grid(row = 6,  column = 2)
root.mainloop()