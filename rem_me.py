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
import calendar # it can help to find day of the week and number of days in month
from tkMessageBox import *

##### Today is ########
day_default = datetime.datetime.now().day
month_default = datetime.datetime.now().month
year_default = datetime.datetime.now().year
hour_default = datetime.datetime.now().hour
minute_default = datetime.datetime.now().minute
weekday_of_firstday, days_in_month = calendar.monthrange(year_default, month_default)

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
	#require = 'INSERT INTO reminders VALUES(null,\"' + str(text) +'", ' +  str(year) +', '+ str(month) +', ' + str(day) + ', ' + str(hour) + ', ' + str(minutes)+ ')'#' + str(id) + ', "'
	t = (text, year, month, day, hour, minutes)
	con = sqlite3.connect('reminders.db')
	cur = con.cursor()
	try:
		cur.execute('INSERT INTO reminders VALUES(null, ?, ?, ?, ?, ?, ?)',t)
		con.commit()
	except sqlite3.IntegrityError:
		print 'This value has been entered into database before!'
	con.close()	

def find_actual_rem( data, year = year_default, month = month_default, day = day_default):
	'''Function controls date_ fields in all tables and find actualy reminders for current day
		This Function must be started with set into deltatime
	'''
	# TODO: 1. Use datetime for search
	t=(year, month, day)
	con = sqlite3.connect('reminders.db')
	cur = con.cursor()
	cur.execute('SELECT textReminder, date_month, date_day, date_hour, date_minute from reminders where date_year = ? and date_month = ? and date_day = ?', t) #  <<<--- old
	#data = cur.fetchall()
	while True:
		tmp = cur.fetchone()
		if tmp:
			data.append(tmp)
		else:
			break
	con.close()
	#print t, ' ===> ', data
	return data

def show_rem(name = u'Test', data=u'Hier your info'):
	'''Function recieves  actual reminder for this time and show it in special bright windows
	'''
	#TODO:	1. Func must show any list with data in right for reading form
	# [           0,          1,        2,         3,           4]
	# [textReminder, date_month, date_day, date_hour, date_minute]
	info = name + ':\n'
	for i in data:
		info += str(i[2]) + '.' + str(i[1]) +'  at' + str(i[3]) + ' : ' + str(i[3]) +'  TODO =>' + str(i[0]) + '\n' 
	info += str(len(data))

	showinfo(name, info)

def save_reminder(event):
	'''Function works when user press to button 'Save' and reads text from the textfield and from the date-fields. 
	If it isn't problem with entered data, call function new_reminder
	'''
	#print 'You call save_reminder function'
	
	control_env_fields(None)
	new_reminder(text = unicode(tx.get('1.0', 'end')), year = ent_year.get(), month = ent_month.get(), day = ent_day.get(), hour = ent_hour.get(), minutes = ent_minute.get())
	#print ent_day.get('1.0', 'end')
	#print text

def error_input(obj, default_value = 1):
		'''Function put in current date in field, if user entered noncorrect data
		'''
		obj.delete(0, END)
		obj.insert(0, default_value)
		res = obj.get()
		obj ['bg'] = 'pink'
		return res

def reminder_today(event):
	'''Function shows all reminders for today
	'''
	# TODO: 1. Must show reminders in special window with comfort for reading form
	result = rem_for_one_day(day_default)
	print 'Rem for today =', len(result),'\n', result
	show_rem(name = u'All Reminders for Today', data = result)
	

def rem_for_one_day(rem_day):
	res = []
	res = find_actual_rem(data = res, day = rem_day )# = day_default)
	print rem_day, res
	return res

	
def reminder_this_week(event):
	'''Function shows all reminders for current week
	'''
	print 'You call reminder_this_week function'
	res = []
	count_day_in_last_month = 0
	if (day_default + 7) <= days_in_month: 			# if all next week only in current month
		print 'in reminder_this_week all day in this month'
		for day in range(day_default, day_default+7):
			res =find_actual_rem(data = res, day=day, month = month_default)
			#res.append(rems) # this method gave noncomfort result as: [((),()),()]. I want to have only list of tuples 
	else:
		print 'in two monthes part 1'
		res_part1 = []
		res_part2 = []
		for day in range(day_default, days_in_month+1):
			res_part1 =find_actual_rem(data = res_part1, day=day, month = month_default)
			#res.append(rems)
			count_day_in_last_month += 1
		if month_default == 12:     # if we will have the part in the end of current year and 2nd part in the next year
			year = year_default + 1
			month = 1
		else:
			year =year_default
			month = month_default + 1
		#print year, month, '-->', res
		
		for day in range(1, 7-count_day_in_last_month):
			res_part2 = find_actual_rem(data = res_part2, day=day, month = month, year = year)
			#if rems:
			#	res.append(rems)
				#print 'emty day'
		res = res_part1 + res_part2
			#print rems, (rems ==True), ' <--->',res
	print 'Rem-s for week =', len(res), res
		#days_for_weekend = weekday_of_firstday
	show_rem(name = u'All Reminders for week:', data = res )

def reminder_this_month(event):
	'''Function return all Reminders for current month
	'''
	print 'You call reminder_this_month function'
	res = []
	for i in range(1, days_in_month+1):
		print 'rem month',res
		res =find_actual_rem(data = res, day = i, month = month_default, year = year_default)
		#if rems:
		#	res.append(rems)
	show_rem(name =u'All Reminders for this month', data = res)

def reminder_all(event):
	'''Show all reminders in database
	'''
	# TODO:	1. Use another window for show res. In it must be: scrollbar, delite-function, selectin with colors old and new reminders and other
	print 'You call reminder_all function'
	res = []
	#res =find_actual_rem(data = res, day = i, month = month_default, year = year_default)
	con = sqlite3.connect('reminders.db')
	cur = con.cursor()
	max_id = counter()
	for i in range(1, max_id+1):
		id_tuple = i,
		print id_tuple
		cur.execute('SELECT textReminder, date_month, date_day, date_hour, date_minute from reminders where id = ?', id_tuple)
		data = cur.fetchall()
		res.append(data)
	con.close()
	show_rem(name =u'All Reminders', data = res)

def control_env_fields(event):
	'''Control and if finds error - makes correctin of values in all Entry-fields.  (ent_year, ent_month, ent_day, ent_hour, ent_minute) 
	'''
	# TODO:	1. Make determination of curren weekday and find all remainders for this week in bd.
	#		2. Reminders for future and tuday must be signed with green color, for last - red!
	
	month = ent_month.get()
	all_entry_fields = ((ent_year, year_default, year_default+10, year_default),
	  					(ent_month, 1, 12, month_default),
	    				(ent_day, 1, days_in_month, day_default),
	     				(ent_hour, 0, 23, hour_default + 1),
	      				(ent_minute, 0, 59, minute_default))
	for field in all_entry_fields:
		print field[0].get()
		try:
			val = int(field[0].get())
		except NameError:
			val = error_input(field[0], field[3])
		except ValueError:
			val = error_input(field[0], field[3])
	
		if not(val>=field[1] and val<=field[2]):
			val = error_input(field[0], field[3])
		print val

def counter():
	'''COunt number of rows in db
	'''
	con = sqlite3.connect('reminders.db')
	cur = con.cursor()
	cur.execute('SELECT count(*) from reminders ')
	m = cur.fetchone()
	cur.execute('SELECT count(*) from reminders where date_day = "1";')
	n = cur.fetchall()
	con.close()
	return m[0]
	

#### Main window ####
print sqlite3.version # currant version sqlite3
create_db()

print datetime.datetime.now().strftime("%d.%m.%Y.%I.%M.%p")
# You can input your reminder in command line with format (after filename must be 6 arguments!):
# ...$ python rem_me.py 'MESSAGE' YEAR MONTH DAY HOUR MIN
if len(sys.argv)>1: reminder_from_cl(len(sys.argv))
	#print len(sys.argv), sys.argv
	
#rem_month = find_actual_rem()
#rem_month = []
#rem_cur_year = find_actual_rem()
#for i in rem_cur_year:
#	if i[2] == 2015 and i[3] == 1:
#		rem_month.append(i)
#	print rem_month
#print rem_month

root = Tk()
root.title(' My reminders')
root.minsize(height = 375, width = 620) # Min size of main window
root.maxsize(height = 375, width = 620) # Max size of main window

lab = Label(root, text = 'Write your reminder hire:', font = 'Verdana 12')
lab.grid(row = 0, column = 0)

tx = Text(root, height = 6, width = 25, bg = 'lightgreen', font = "Verdana 14",	wrap = WORD) # textfield
tx.grid(row = 1, column = 0, sticky='nsew')

lab = Label(root, text = 'Write date:', font = 'Verdana 12')
lab.grid(row = 0, column = 1)

#fra = Frame(root, height = 80, width = 700, bg = 'green')
#fra.grid(row = 3, column = 0)
lab = Label(root, text = 'Year:', font = 'Verdana 10')
lab.grid(row = 2, column = 1)

ent_year = Entry(root, width = 4, bd = 2, bg = 'white')
ent_year.insert(0, year_default)
ent_year.grid(row = 2, column = 2)
#ent_day.bind('<Motion>', reminder_today)
#ent_day.pack()

lab = Label(root, text = 'Month:', font = 'Verdana 10')
lab.grid(row = 3, column = 1)

ent_month = Entry(root, width = 4, bd = 2)
ent_month.insert(0, month_default)
ent_month.grid(row = 3, column = 2)

lab = Label(root, text = 'Day:', font = 'Verdana 10')
lab.grid(row = 4, column = 1)

ent_day = Entry(root, width = 4, bd = 2)
ent_day.insert(0, day_default)
ent_day.grid(row = 4, column = 2)

lab = Label(root, text = 'Hour:', font = 'Verdana 10')
lab.grid(row = 5, column = 1)

ent_hour = Entry(root, width = 4, bd = 2)
ent_hour.insert(0, hour_default+1)
ent_hour.grid(row = 5, column = 2)

lab = Label(root, text = 'Minutes:', font = 'Verdana 10')
lab.grid(row = 6, column = 1)

ent_minute = Entry(root, width = 4, bd = 2)
ent_minute.insert(0, minute_default)
ent_minute.grid(row = 6, column = 2)

##### BUTTONS #####
but1 = Button(root, height = 1, width = 20, font = 'Verdana 20', bg = 'gold', activebackground = 'green')
but1['text'] = "Save"
but1.bind('<Button-1>', save_reminder)
but1.grid(row = 2,  column = 0)

but2 = Button(root)
but2['text'] = "Rem for day"
but2.bind('<Button-1>', reminder_today)
but2.grid(row = 7,  column = 0)

but3 = Button(root)
but3['text'] = "Rem for week"
but3.bind('<Button-1>', reminder_this_week)
but3.grid(row = 7,  column = 1)

but4 = Button(root)
but4['text'] = "Rem for month"
but4.bind('<Button-1>', reminder_this_month)
but4.grid(row = 7,  column = 2)

but5 = Button(root)
but5['text'] = "Cntrl fields"
but5.bind('<Button-1>', control_env_fields)
but5.grid(row = 8,  column = 0)

but6 = Button(root)
but6['text'] = "Rem ALL"
but6.bind('<Button-1>', reminder_all)
but6.grid(row = 8,  column = 1)

print 'Therenis:', counter(), 'records in database'
root.mainloop()