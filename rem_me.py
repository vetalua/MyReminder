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
import datetime
import calendar # it can help to find day of the week and number of days in month
from tkMessageBox import *
import threading
from time import gmtime, strftime
import random

######################################################################################################## Today is ########
def refrash_date():
	'''Function refrash time and day and return it
	'''
	day_now 	= datetime.datetime.now().day
	month_now 	= datetime.datetime.now().month
	year_now 	= datetime.datetime.now().year
	hour_now 	= datetime.datetime.now().hour
	minute_now 	= datetime.datetime.now().minute
	second_now 	= datetime.datetime.now().second
	return (year_now, month_now, day_now, hour_now, minute_now, second_now)


####################################################################### Day of week, days in month,  dict names of monthes
day_default = datetime.datetime.now().day
month_default = datetime.datetime.now().month
year_default = datetime.datetime.now().year
hour_default = datetime.datetime.now().hour
minute_default = datetime.datetime.now().minute
weekday_of_firstday, days_in_month = calendar.monthrange(year_default, month_default)
weekday_of_firstday, days_in_month = calendar.monthrange(year_default, month_default)
month_name = {1:'Jan.', 2:'Feb.', 3:'Mar.', 4:'Apr.', 5:'May', 6:'Jun.', 7:'Jul.', 8:'Aug.', 9:'Sept.', 10:'Oct.', 11:'Nov.', 12:'Dec.'}
show_done = True 
# Set show_done = True after start programe. It's make posible don't start timer,
# if set show_done to False or status(rem_actual[7]) to False

rem_actual = [] # reminders wich must be shown today, after start it is empty list

###########################################################################################################    FUNCTIONS

def create_db():
	'''Function creates database Sqlite3 with name: 'reminders.db'  if it's absent in dirrectory with this program
	'''
	# TODO: 1. id must be automaticaly 									- DONE
	#		2. Another fields must be adding (rem for avryyear or no)!  - DONE
	#		3. Add seconds to db!  										- DONE
	#		4. Add status-field of message into db: if shown, field = 1. if skip field=0  - rem_actual[7]
	#show_status (u'Connect to database') # with this string we have Traceback (most recent call last): NameError: global name 'status' is not defined. WHY?
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
	 		 date_second INTEGER,
	 		 type_reminder VARCHAR(50) not null,
	 		 timestamp not null,
				unique (textReminder))''')
		con.commit()
		new_reminder(type_reminder = u'evry year')
		print 'Creating db had done'
	except sqlite3.OperationalError:
		print 'reminders.db had made before'
	finally:
		if con:
			con.close()

def reminder_from_cl(len_args):
	'''Function works with values wich had entered from comand line. You can don't use  this method, but use entering with GUI
	'''
	#TODO:	1. Use arguments with names 					- DONE
	#		2. Every year reminder can be entered only with comand line. Make a button for select 'YEARLY' or 'ONE TIME'
	#show_status (u'Receive Reminder from Comand line') - don't work
	if len_args == 2:
		new_reminder(text = sys.argv[1])
	else:
		try:
			new_reminder(text = sys.argv[1], year = sys.argv[2], month = sys.argv[3], day = sys.argv[4], hour = sys.argv[5], minutes = sys.argv[6], type_reminder = u'YEARLY')
		except IndexError:
			print 'You must input 6 arguments for entering with comand line!'	

def new_reminder(text = 'New Year', year = year_default, month = month_default, day = day_default, hour = hour_default + 1, minutes = minute_default, second = 0, type_reminder = u'ONE TIME'):
	'''Function controls text of new reminder: if text not new - write it in new message in window,
		if new reminder - write it to database (other fields must be full with information, defaults values are current time + 1 hour )
	'''	
	#	TODO: 	1.Use timedelta for writing data in db 			- DONE
	#			2. Must do update field type_reminder, for signal about appearing reminder or about skip ot in last
	#			3. For every year reminder after appearing must be change year in db (year = year + 1)
	#show_status (u'Adding New Reminder to db')			# - not work?
	
	time_creating = str(refrash_date()) # for wrighting creating time reminder
	v = c1.get()
	if v ==1:
		type_reminder = 'YEARLY'  # For every yeary reminders. Work if set Checkbutton che1
	t = (text, year, month, day, hour, minutes, second, type_reminder, time_creating) 
	con = sqlite3.connect('reminders.db')
	cur = con.cursor()
	try:
		cur.execute('INSERT INTO reminders VALUES(null, ?, ?, ?, ?, ?, ?, ?, ?, ?)', t)
		con.commit()
	except sqlite3.IntegrityError:
		print 'This value has been entered into database before or some other problems with writting!'
	finally:
		con.close()
	return (text, year, month, day, hour, minutes, second, type_reminder)

def find_actual_rem( data, year = year_default, month = month_default, day = day_default):
	'''Function controls date_ fields in all tables and find actualy reminders for current day
		This Function must be started with set into deltatime
	'''
	# TODO: 1. Use datetime for search - Searching work normal now. 	- DONE
	show_status (u'Finding actual to ' + str(day) + '.'+ str(month)+'.'+str(year) )
	t=(year, month, day)
	con = sqlite3.connect('reminders.db')
	cur = con.cursor()
	cur.execute('SELECT textReminder, date_month, date_day, date_hour, date_minute, date_second, type_reminder from reminders where date_year = ? and date_month = ? and date_day = ? order by date_year, date_month, date_day, date_hour, date_minute, date_second', t) #  <<<--- old
	#data = cur.fetchall()
	while True:
		tmp = cur.fetchone()
		if tmp:
			data.append(tmp)
		else:
			break
	con.close()
	return data

def show_rem(name = u'Test', data=u'Here your info'):
	'''Function recieves  reminders  wich user require with button  and show it in standart window
	'''
	#TODO:	1. Func must show any list with data in right for reading form - DONE.
	# Data consist of:
	# [           0,          1,        2,         3,           4,           5,             6]
	# [textReminder, date_month, date_day, date_hour, date_minute, date_second, type_reminder]
	
	show_status (u'Show info:' + name)
	if data:
		info = '   All:' + str(len(data)) + ' reminders \n'
		for i in data:
			info += str(i[2]) + ' ' + month_name[i[1]] +'  at ' + str(i[3]) + ':' + str(i[4]) +':' + str(i[5]) +'  => ' + str(i[0]) + '\n' 
	else:
		info = '   All:' + str(len(data)) + '\n Reminders list is empty\n'	
	showinfo(name, info)

def save_reminder(event):
	'''Function works when user press to button 'Save' and reads text from the textfield and from the date-fields. 
	If it isn't problem with entered data, call function new_reminder for saving to database
	'''	
	# TODO: 1. Must control new reminder, if it for today, 
	# 			must add it to rem_act (and) start new treading if it first in list - DONE
	#		2. See comment in 176 string!!!                                         - DONE
	#global rem_actual
	show_status (u'Saving reminder')
	control_env_fields(None)
	second_rand = random.randint(0, 59)
	t = new_reminder(text = unicode(tx.get('1.0', 'end')), year = ent_year.get(), month = ent_month.get(), day = ent_day.get(), hour = ent_hour.get(), minutes = ent_minute.get(), second = second_rand)
	newest_rem = list(t)
	tx.delete('1.0', 'end')
	print 'in save_reminder, rem_actual:', rem_actual
	for i in range(1,6): # HERE SOME BUG: If reminder is not for today - it put in only to DB, but not to rem_actual list!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		newest_rem[i] = int(newest_rem[i])	# from string to integer
	insert_newest_rem(newest_rem)
	if rem_actual:
		delta_seconds_to_show = seconds_to_show_reminder(rem_actual[0]) # call seconds_to_show_reminder, which return the number of seconds to show reminder
		start_treading(delta_seconds_to_show)

def insert_newest_rem(newest_rem):
	'''Function insert new reminder to list actual_rem on it place, ordered by time
	'''
	#             (         0,         1,       2,        3,           4,            5 )
	# refresh_now (  year_now, month_now, day_now, hour_now,  minute_now,    second_now)
	# newest =    (      text,      year,   month,      day,        hour,       minutes, second, type_reminder)
	# format =    [textReminder, date_month, date_day, date_hour, date_minute, date_second, type_reminder]
	global show_done
	now = refrash_date()
	#print now, 'IN insert_newest_rem'
	#print newest_rem
	#print newest_rem[2], '== ', now[1], ' and ', newest_rem[3], ' == ', now[2], ' type newest_rem -', type(newest_rem[3]), ' type now -', type(now[2])
	if newest_rem[1] == now[0] and newest_rem[2] == now[1] and newest_rem[3] == now[2]	: # control year, month and day of newest_reminder
		show_status(u'Insert new reminder into rem_actual')
		print newest_rem[4], ' >= ', now[3], ' and ', newest_rem[5],' > ', now[4]
		del newest_rem[1]
		newest_rem.append(True) # new_rem must have status True for starting in treading
		if (newest_rem[3] > now[3]) or (newest_rem[3] == now[3] and newest_rem[4] > now[4]):
			print 'MUST INSERT TO LIST rem_actual newest_rem'
			#TODO:  find place and insert to rem_actual, create right format(del year, insert status....)   - DONE
			ind = find_place_index(newest_rem)
			if ind == 0:
				show_done = True
				print 'ind =', ind, '===>   show_done = ', show_done
			rem_actual.insert(ind, newest_rem)
	print 'rem_actual at end:  ', rem_actual

def find_place_index(newest_rem):
	'''Returns num, whish equal to index for insert new reminder into rem_actual
	'''
	num = 0
	show_status (u'Finding index for insert')
	print 'find_place_index was started rem_actual = ', rem_actual
	if rem_actual !=[]:
		for i in rem_actual:
			print i
			if (newest_rem[3] == i[3] and newest_rem[4] < i[4]) or (newest_rem[3]<i[3]):
				print 'find_place_index num = ', num
				return num
			num +=1
		print 'find_place_index num = ', num		
	return num

def error_input(obj, default_value = 1):
	'''Function put current date in field, if user entered noncorrect data 
	'''
	show_status (u'Finding errors in date-fields')
	obj.delete(0, END)
	obj.insert(0, default_value)
	res = obj.get()
	obj ['bg'] = 'pink'
	return res

def reminder_today(event, window_show = True, window_skiped = True):
	'''Function shows all reminders for today
	'''
	global rem_actual
	show_status (u'Finding Reminders for today')
	day_now = refrash_date()[2]
	result = rem_for_one_day(day_now)
	if result:
		res = next_autoshow_rem(result)
		print 'REM SKIPED  ----------->', len(res[0])
		print 'REM ACTUAL  ----------->', len(res[1]), '\n', res[1]
		if res[1]:
			print 'NEXT reminder --------->', res[1][0]
			if rem_actual == []:
				rem_actual = res[1]
				delta_seconds_to_show = seconds_to_show_reminder(res[1][0]) # call seconds_to_show_reminder, wich return the nomber of seconds to show reminder
				start_treading(delta_seconds_to_show)
		if window_show:
			show_rem(name = u'All actual Reminders for Today', data = rem_actual) # window with result will show only if window_show=True
		if res[0] and window_skiped:
			for rem in res[0]:
				if rem[6] != u'DONE':
					reminder_window(rem)
			#show_rem(name = u'All SKIPED Reminders for Today', data = res[0]) # For show skipped reminders (only if it is in list res[0])	
	else:
		res = None
		# maybe here must be add a reminder at 0:00 next day
		if window_show:
			show_rem(name = u'All actual Reminders for Today', data = [])

	
	return res
	

def rem_for_one_day(rem_day):
	'''Function get rem_day for searching in database of all reminders for this rem_day 
	'''
	show_status (u'Finding Reminders for day - ' + unicode(rem_day))
	res = []
	res = find_actual_rem(data = res, day = rem_day )
	print 'SEARCH IN DB reminders for day ',rem_day
	return res

	
def reminder_this_week(event):
	'''Function shows all reminders for current day to 7 next days
	'''
	res = []
	count_day_in_last_month = 0
	show_status (u'Finding Reminders for this week')
	if (day_default + 7) <= days_in_month: 			# if all next week only in current month
		for day in range(day_default, day_default+7):
			res =find_actual_rem(data = res, day=day, month = month_default)
	else:
		res_part1 = []
		res_part2 = []
		for day in range(day_default, days_in_month+1):
			res_part1 =find_actual_rem(data = res_part1, day=day, month = month_default)
			count_day_in_last_month += 1
		if month_default == 12:     # if we will have the 1 part in the end of current year and 2nd part in the next year
			year = year_default + 1
			month = 1
		else:
			year =year_default
			month = month_default + 1
				
		for day in range(1, 7-count_day_in_last_month):
			res_part2 = find_actual_rem(data = res_part2, day=day, month = month, year = year)
		res = res_part1 + res_part2
	show_rem(name = u'All Reminders for week:', data = res )

def reminder_this_month(event):
	'''Function return all Reminders for current month
	'''
	show_status (u'Finding Reminders for month')
	res = []
	for i in range(1, days_in_month+1):
		res =find_actual_rem(data = res, day = i, month = month_default, year = year_default)
	show_rem(name =u'All Reminders for this month', data = res)

def reminder_all(event):
	'''Show all reminders in database
	'''
	# TODO:	1. Use another window for show res. In it must be: scrollbar, delite-function, selectin with colors old and new reminders and other
	show_status (u'Finding ALL Reminders')
	res = []
	con = sqlite3.connect('reminders.db')
	cur = con.cursor()
	max_id = counter()
	for i in range(1, max_id+1):
		id_tuple = i,
		#print id_tuple
		cur.execute('SELECT textReminder, date_month, date_day, date_hour, date_minute, date_second, type_reminder from reminders where id = ?', id_tuple)
		data = cur.fetchone()
		if data:			# if reminder had cut from database, this func return None. I control data for solving problems 
			res.append(data)
	con.close()
	show_rem(name =u'All Reminders', data = res)

def control_env_fields(event):
	'''Control and if finds error - makes correctin of values in all Entry-fields.  (ent_year, ent_month, ent_day, ent_hour, ent_minute) 
	'''
	# TODO:	1. Make determination of curren weekday and find all remainders for this week in bd. - I am not sure that must do now
	#		2. Reminders for future and today must be signed with green color, for last - red!
	show_status (u'Controll values in date-fields')
	month = ent_month.get()
	now = refrash_date() 
	# (       0,         1,       2,        3,          4,          5)
	# (year_now, month_now, day_now, hour_now, minute_now, second_now)
	all_entry_fields = ((ent_year, year_default, year_default+10, now[0]),  # consist of Entry (year, month, day, hour,minute), and determining values for min, max, default to everyone of it
	  					(ent_month, 1, 12, now[1]),
	    				(ent_day, 1, days_in_month, now[2]),
	     				(ent_hour, 0, 23, now[3] + 1),
	      				(ent_minute, 0, 59, now[4]))
	for field in all_entry_fields:
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
	'''Count number of rows in db
	'''
	con = sqlite3.connect('reminders.db')
	cur = con.cursor()
	cur.execute('SELECT count(*) from reminders ')
	m = cur.fetchone()
	cur.execute('SELECT count(*) from reminders where date_day = "1";')
	n = cur.fetchall()
	con.close()
	return m[0]

def next_autoshow_rem(data):
	''' Fuction finds skiped reminders (creates a list), actual reminders (create a list) and next reminder
	'''
	# Data consist of:
	# [           0,          1,        2,         3,           4,           5,             6]
	# [textReminder, date_month, date_day, date_hour, date_minute, date_second, type_reminder]
	rem_actual_today = []
	rem_skiped_today = []
	# USE data from func refrash_date in the circle
	now = refrash_date()
	#hour_now = now[3]

	for rem in data:
		if rem[3]<now[3]:
			#print rem[3], ' < ', hour_default
			rem_skiped_today.append(rem)
		if rem[3] == now[3]:#hour_default:
			if rem[4] <= now[4]:#minute_default:
				
				rem_skiped_today.append(rem)
			if rem[4] > now[4]:#minute_default:
				rem_list = list(rem)
				rem_list.append(True) # last element of list - is a saignal, that threading was started or wasn't
				rem_actual_today.append(rem_list)
		if rem[3] > now[3]:#hour_default:
			#print rem[3], ' > ', hour_default
			rem_list = list(rem)
			rem_list.append(True)
			rem_actual_today.append(rem_list)
	if rem_actual_today:
		next_rem = rem_actual_today[0]
		print 'We have actual reminders today'
	else:
		next_rem = None
		showinfo(u'All actual Reminders for Today', u'No Reminder today')
	print 'end next_autoshow_rem function'
	if next_rem:
		show_status (next_rem[0])
	else:
		show_status('No next reminder today')
	return [rem_skiped_today, rem_actual_today]
	

def show_status(message = u'treading'):
	'''Function writes message in status window
	'''
	status['text'] = 'Last operation: ' + str(message)

def seconds_to_show_reminder(next_rem):
	'''Function counts how many seconds for show next reminder to screen
	'''
	#TODO: 1. Use seconds for counting delta_seconds! Maybe seconds must be used always, where we used minute, hour,
	# 	... in db too!
	# [           0,          1,        2,         3,           4,           5,             6,        7]
	# [textReminder, date_month, date_day, date_hour, date_minute, date_second, type_reminder,   status]
	now 		= refrash_date()
	hour_now 	= now[3]
	minute_now 	= now[4]
	second_now 	= now[5]

	if next_rem[4]>=minute_now:
		delta_seconds = ((next_rem[3] - hour_now)*60*60) + ((next_rem[4] - minute_now)*60) + (next_rem[5] - second_now)
		print '(', next_rem[3], '-', hour_now,') *3600 + (', next_rem[4], '-', minute_now,')*60 +(', next_rem[5], '-', second_now, ') ===', delta_seconds 
	else:
		delta_seconds = ((next_rem[3] - hour_now)*60*60) - ((minute_now - next_rem[4])*60) + (next_rem[5] - second_now)
		print '(', next_rem[3], '-', hour_now,') *3600 - (', minute_now, '-', next_rem[4],')*60 +(', next_rem[5], '-', second_now, ') ===', delta_seconds
	return delta_seconds

def show_message_treading():
	'''Function writes message in status window
	'''
	# TODO : 1. Function must change rem_actual[0][6] to 'DONE' if it shown and have atribute 'One to future', 
	#			or must be changed atr date_year (+1) in DB
	#status['text'] = 'Last operation: treading'
	print 'IT IS TIME TO DO: ', str(rem_actual[0][0])
	reminder_window(rem_actual[0])
	global show_done
	show_done = True
	print strftime("[%H:%M:%S]", gmtime()) + " show_done = ", show_done
	del rem_actual[0]
	print 'rem_actual was reduced with del -->', rem_actual
	if rem_actual:
		print 'in show_message_treading - call start_treading/ send -', rem_actual[0]
		delta_seconds_to_show = seconds_to_show_reminder(rem_actual[0]) # call seconds_to_show_reminder, wich return the nomber of seconds to show reminder
		start_treading(delta_seconds_to_show)

def reminder_window(rem):
	'''Show bright window with text of reminder
	'''
	def ok_func(event):
		'''Start after click on button OK in reminder window: change type reminder (ONE -> DONE) or update rem in DB (+1 year) 
		'''
		if rem[6] == u'ONE TIME':
			t = (u'DONE', datetime.datetime.now().year, rem[0], rem[1], rem[2])
		else:
			t = (rem[6], datetime.datetime.now().year +1, rem[0], rem[1], rem[2])
		print 'UPDATing with t =', t 
		try:
			con = sqlite3.connect('reminders.db')
			cur = con.cursor()
			cur.execute('UPDATE reminders SET type_reminder=?, date_year = ? WHERE textReminder=? AND date_month=? AND date_day=?', t)
			con.commit()
			print 'COMMIT'
		except sqlite3.IntegrityError:
			print 'This value has been entered into database before or some other problems with writting!'
		finally:
			if con:
				con.close()
		win.destroy()
	
	def add_5min(event):
		'''Start after click on button +5 min in reminder window: change date reminder in DB (+5 min) 
		'''
		time_new = datetime.datetime.now() + datetime.timedelta(seconds = 300)
		timetuple =time_new.year, time_new.month, time_new.day, time_new.hour, time_new.minute, rem[0]
		try:
			con = sqlite3.connect('reminders.db')
			cur = con.cursor()
			cur.execute('UPDATE reminders SET date_year=?, date_month=?, date_day=?, date_hour=?, date_minute=? WHERE textReminder=?', timetuple)
			con.commit()
			print 'COMMIT'
		except sqlite3.IntegrityError:
			print 'This value has been entered into database before or some other problems with writting!'
		finally:
			if con:
				con.close()
		reminder_today(None, window_show = False, window_skiped = False)
		win.destroy()

	def del_func(event):
		'''Start after click on button del_func in reminder window: delete field from DB
		'''
		data_del_reminder = rem[0], rem[1], rem[2]
		try:
			con = sqlite3.connect('reminders.db')
			cur = con.cursor()
			print 'start Delete'
			cur.execute('DELETE from reminders WHERE textReminder=? AND date_month=? AND date_day=?', data_del_reminder)
			con.commit()
			print 'COMMIT'
		except sqlite3.IntegrityError:
			print 'Operation called exception!'
		finally:
			if con:
				con.close()
		reminder_today(None, window_show = False, window_skiped = False)
		win.destroy()		

	# TODO:		1. Maybe window must have to button:
	#				1) 'OK' 				-  reminder was written and must be change rem_actual[0][6]
	#				2) 'Remind me later'  	-	reminder will be show again by 5 min. (for example)
	#			2. Work space for text must be lower - as size of win!
	color = random.choice(['lightblue', 'lightgreen', 'pink', 'red', 'yellow', 'gold', 'blue'])
	win = Toplevel(root, relief = SUNKEN, bd=10, bg = color)
	win.title(str(rem[3]) + ':' + str(rem[4]) + ' REMINDER for NOW')
	win.minsize(width = 250, height = 250)
	#win.maxsize(width = 250, height = 250)
	
	if len(str(rem[3]))==1:
		HHMM = '0'+ str(rem[3])
	else:
		HHMM = str(rem[3])
	if len(str(rem[4]))==1:
		HHMM = HHMM +':0'+ str(rem[4])
	else:
		HHMM = HHMM +':'+ str(rem[4])
	mes = Label(win, font = 'Arial 18', bg = color, text = (HHMM +'\n' + '*'*24 + '\n' + str(rem[0]) + '\n'*2 + '*'*25))
	mes.pack()
	butOK = Button(win, text = 'OK')
	butOK.pack()
	butOK.bind('<Button-1>', ok_func)
	but5min = Button(win, text = '+5 min')
	but5min.pack()
	but5min.bind('<Button-1>', add_5min)
	but_del = Button(win, text = 'DEL')
	but_del.pack()
	but_del.bind('<Button-1>', del_func)
	
		
def start_treading(delta_seconds):
	'''TREADING FUNCTION - counts delta_seconds and then show Text of Reminder on screen
	'''
	global show_done
	print 'calling start_treading: show_done = ', show_done

	if show_done == True and rem_actual[0][7] == True:
		timer = threading.Timer(delta_seconds, show_message_treading)
		timer.start()
		show_done = False
		rem_actual[0][7] = False
		print 'IN start_treading text glboal lists. Actual: ', rem_actual
		print strftime("[%H:%M:%S]", gmtime()) + " Start \n show_done = ", show_done
	else:
		print strftime("[%H:%M:%S]", gmtime()) + " NOT START"

def next_day_control():
	''' Function controles default time for reminder and if it is 23 hour - show 0 hour of next day
	'''
	if hour_default >= 23: 				# this is control error in time (24 hour, 32 day, 13 month).It error was able bicose hour = hour_default +1
		hour_default_entry = 0
		day_default_entry = day_default + 1
		if day_default_entry > days_in_month:
			day_default_entry = 1
			month_default_entry = month_default + 1
		else:
			month_default_entry = month_default
		if month_default_entry > 12:
			month_default_entry = 1
			year_default_entry = year_default + 1
		else:
			year_default_entry = year_default
	else:
		hour_default_entry = hour_default + 1
		day_default_entry = day_default
		month_default_entry = month_default
		year_default_entry = year_default
	print 'Result next_day_control: ', hour_default_entry, day_default_entry, month_default_entry, year_default_entry
	return (hour_default_entry, day_default_entry, month_default_entry, year_default_entry)

########################################################################################################################

create_db()
print datetime.datetime.now().strftime("%d.%m.%Y.%I.%M.%p") # servicing info
#status_first = str(sqlite3.version) + '\n' + str(datetime.datetime.now().strftime("%d.%m.%Y.%I.%M.%p"))
print refrash_date()
print day_default, ' From refrash_date function'

# You can input your reminder in command line with format (after filename must be 6 arguments!):
# ...$ python rem_me.py 'MESSAGE' YEAR MONTH DAY HOUR MIN

if len(sys.argv)>1:
	reminder_from_cl(len(sys.argv))

###################################################################################################### Main window ####

# TODO:		1. Cozy design of window !!!!	
root = Tk()
root.title(' My reminders')
root.minsize(height = 300, width = 550) # Min size of main window
root.maxsize(height = 300, width = 550) # Max size of main window

lab = Label(root, text = 'Write your reminder here:', font = 'Verdana 12')
lab.grid(row = 0, column = 0, columnspan = 4)

tx = Text(root, height = 6, width = 25, bg = 'lightgreen', font = "Verdana 14",	wrap = WORD) # textfield
tx.grid(row = 1, column = 0, sticky='nsew', rowspan = 5, columnspan = 4, padx = 3, pady = 3)

lab = Label(root, text = 'Select date:', font = 'Verdana 12')
lab.grid(row = 0, column = 4, columnspan = 2)

lab = Label(root, text = 'Year:', font = 'Verdana 10')
lab.grid(row = 1, column = 4)

#w = Canvas(root, width = 220, height = 150)
#w.create_line(0, 150, 220, 0, fill="red", dash=(4, 4))
#w.create_text(22,12, text = 'HARM')
#w.create_window(30,40) 									# not work!!!!
#w.grid(row = 1, column = 1, columnspan = 2)

hour_default_entry, day_default_entry, month_default_entry, year_default_entry = next_day_control()

ent_year = Entry(root, width = 4, bd = 2, bg = 'white')
ent_year.insert(0, year_default_entry)
ent_year.grid(row = 1, column = 5)

lab = Label(root, text = 'Month:', font = 'Verdana 10')
lab.grid(row = 2, column = 4)

ent_month = Entry(root, width = 4, bd = 2)
ent_month.insert(0, month_default_entry)
ent_month.grid(row = 2, column = 5)

lab = Label(root, text = 'Day:', font = 'Verdana 10')
lab.grid(row = 3, column = 4)

ent_day = Entry(root, width = 4, bd = 2)
ent_day.insert(0, day_default_entry)
ent_day.grid(row = 3, column = 5)

lab = Label(root, text = 'Hour:', font = 'Verdana 10')
lab.grid(row = 4, column = 4)

ent_hour = Entry(root, width = 4, bd = 2)
ent_hour.insert(0, hour_default_entry)
ent_hour.grid(row = 4, column = 5)

lab = Label(root, text = 'Minutes:', font = 'Verdana 10')
lab.grid(row = 5, column = 4)

ent_minute = Entry(root, width = 4, bd = 2)
ent_minute.insert(0, minute_default)
ent_minute.grid(row = 5, column = 5)

##### BUTTONS #####
but1 = Button(root, height = 1, width = 24, font = 'Verdana 18', bg = 'yellow', activebackground = 'green')
but1['text'] = "Save"
but1.bind('<Button-1>', save_reminder)
but1.grid(row = 7,  column = 0, columnspan = 4)

but2 = Button(root, height = 1, width = 10, font = 'Verdana 8', bg = 'lightblue', activebackground = 'green')
but2['text'] = "Rem for day"
but2.bind('<Button-1>', reminder_today)
but2.grid(row = 8,  column = 0)

but3 = Button(root, height = 1, width = 10, font = 'Verdana 8', bg = 'lightblue', activebackground = 'green')
but3['text'] = "Rem for week"
but3.bind('<Button-1>', reminder_this_week)
but3.grid(row = 8,  column = 1)

but4 = Button(root, height = 1, width = 10, font = 'Verdana 8', bg = 'lightblue', activebackground = 'green')
but4['text'] = "Rem for month"
but4.bind('<Button-1>', reminder_this_month)
but4.grid(row = 8,  column = 2)

#but5 = Button(root)
#but5['text'] = "Cntrl fields"
#but5.bind('<Button-1>', control_env_fields)
#but5.grid(row = 8,  column = 0)

but6 = Button(root, height = 1, width = 10, font = 'Verdana 8', bg = 'lightblue', activebackground = 'green')
but6['text'] = "Rem ALL"
but6.bind('<Button-1>', reminder_all)
but6.grid(row = 8,  column = 3)

c1 = IntVar()
che1 = Checkbutton(root, text='Every year', variable=c1, onvalue=1, offvalue=0)
#che1.select()
che1.grid(row = 6, column = 3)

fra = Frame(root, height = 25, width = 400, bg = 'white') # as status window in the bootom of window
fra.grid(row = 9, column = 0, columnspan = 7)
status = Label(fra, text = 'Starting: '+ str(counter()) +' Reminders in DB \n Now: '
	+ str(datetime.datetime.now().strftime("%d.%m.%Y.%I.%M.%p")), font = 'Verdana 8', justify = 'left', bg = 'white')
status.grid(row = 0, column = 0)

reminder_today(None, window_show = False)

print 'There is:', counter(), 'records in database'
root.mainloop()