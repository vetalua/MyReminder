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

######################################################################################################## Today is ########
def refrash_date():
	'''Function refrash time and day and return it
	'''
	day_now = datetime.datetime.now().day
	month_now = datetime.datetime.now().month
	year_now = datetime.datetime.now().year
	hour_now = datetime.datetime.now().hour
	minute_now = datetime.datetime.now().minute
	return (year_now, month_now, day_now, hour_now, minute_now)


####################################################################### Day of week, days in month,  dict names of monthes
day_default = datetime.datetime.now().day
month_default = datetime.datetime.now().month
year_default = datetime.datetime.now().year
hour_default = datetime.datetime.now().hour
minute_default = datetime.datetime.now().minute
weekday_of_firstday, days_in_month = calendar.monthrange(year_default, month_default)
weekday_of_firstday, days_in_month = calendar.monthrange(year_default, month_default)
month_name = {1:'Jan.', 2:'Feb.', 3:'Mar.', 4:'Apr.', 5:'May', 6:'Jun.', 7:'Jul.', 8:'Aug.', 9:'Sept.', 10:'Oct.', 11:'Nov.', 12:'Dec.'}
#current_time = str(datetime.datetime.now().strftime("%d.%m.%Y.%I.%M.%p")
show_done = True # set in True after start programe. It's make posible to start timer, which set show_done to False
###########################################################################################################    FUNCTIONS
def create_db():
	'''Function creates database Sqlite with name: 'reminders.db'  if it's absent in dirrectory with this program
	'''
	# TODO: 1. id must be automaticaly - Done
	#		2. Another fields must be adding (rem for avryyear or no)!
	#		3. Add seconds to db!
	#		4. Add status-field of message into db: if shown, field = 1. if skip field=0
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
	#show_status (u'Receive Reminder from Comand line')
	if len_args == 2:
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
	# show_status (u'Adding New Reminder to db')
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
	# TODO: 1. Use datetime for search - Searching work normal now.
	show_status (u'Finding actual to ' + str(day) + '.'+ str(month)+'.'+str(year) )
	t=(year, month, day)
	con = sqlite3.connect('reminders.db')
	cur = con.cursor()
	cur.execute('SELECT textReminder, date_month, date_day, date_hour, date_minute from reminders where date_year = ? and date_month = ? and date_day = ? order by date_year, date_month, date_day, date_hour, date_minute', t) #  <<<--- old
	#data = cur.fetchall()
	while True:
		tmp = cur.fetchone()
		if tmp:
			data.append(tmp)
		else:
			break
	con.close()
	return data

def show_rem(name = u'Test', data=u'Hier your info'):
	'''Function recieves  reminder wich user require with button  and show it in windows
	'''
	#TODO:	1. Func must show any list with data in right for reading form - DONE.
	# Data consist of:
	# [           0,          1,        2,         3,           4]
	# [textReminder, date_month, date_day, date_hour, date_minute]
	show_status (u'Show info:' + name)
	info = '   All:' + str(len(data)) + ' reminders \n'
	for i in data:
		info += str(i[2]) + ' ' + month_name[i[1]] +'  at ' + str(i[3]) + ':' + str(i[4]) +'  => ' + str(i[0]) + '\n' 
	

	showinfo(name, info)

def save_reminder(event):
	'''Function works when user press to button 'Save' and reads text from the textfield and from the date-fields. 
	If it isn't problem with entered data, call function new_reminder for saving to database
	'''	
	# TODO: 1. Must control new reminder, if it for today, must add it to rem_act (and) start new treading(!?)
	show_status (u'Saving reminder')
	control_env_fields(None)
	new_reminder(text = unicode(tx.get('1.0', 'end')), year = ent_year.get(), month = ent_month.get(), day = ent_day.get(), hour = ent_hour.get(), minutes = ent_minute.get())
	#print ent_day.get('1.0', 'end')
	#print text

def error_input(obj, default_value = 1):
	'''Function put current date in field, if user entered noncorrect data 
	'''
	show_status (u'Finding errors in date-fields')
	obj.delete(0, END)
	obj.insert(0, default_value)
	res = obj.get()
	obj ['bg'] = 'pink'
	return res

def reminder_today(event):
	'''Function shows all reminders for today
	'''
	global rem_actual
	show_status (u'Finding Reminders for today')
	# TODO: 1. Must show reminders in special window with comfort for reading form - DONE in function show_rem
	day_now = refrash_date()[2]
	result = rem_for_one_day(day_now)
	#print 'Rem for today =', len(result),'\n', result
	#show_rem(name = u'All Reminders for Today', data = result)
	if result:
		res = next_autoshow_rem(result)
		if res[1]:
			print 'NEXT reminder --------->', res[1][0]

		print 'REM SKIPED  ----------->', res[0] 
		print 'REM ACTUAL  ----------->', res[1]
		if res[1]:
			rem_actual = res[1]
			delta_seconds_to_show = seconds_to_show_reminder(res[1][0]) # call seconds_to_show_reminder, wich return the nomber of seconds to show reminder
			start_treading(delta_seconds_to_show)

	else:
		res = None
		show_rem(name = u'All actual Reminders for Today', data = u'List of reminders for today is empty')
	return res
	

def rem_for_one_day(rem_day):
	'''Function get rem_day for searching in database of all reminders for this rem_day 
	'''
	show_status (u'Finding Reminders for day - ' + unicode(rem_day))
	res = []
	res = find_actual_rem(data = res, day = rem_day )# = day_default)
	print 'SEARCH IN DB reminders for day '#,rem_day,'--->', res
	return res

	
def reminder_this_week(event):
	'''Function shows all reminders for current current day to 7 next days
	'''
	res = []
	count_day_in_last_month = 0
	show_status (u'Finding Reminders for this week')
	if (day_default + 7) <= days_in_month: 			# if all next week only in current month
		#print 'in reminder_this_week all day in this month'
		for day in range(day_default, day_default+7):
			res =find_actual_rem(data = res, day=day, month = month_default)
	else:
		#print 'in two monthes part 1'
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
	#print 'Rem-s for week =', len(res), res
	show_rem(name = u'All Reminders for week:', data = res )

def reminder_this_month(event):
	'''Function return all Reminders for current month
	'''
	show_status (u'Finding Reminders for month')
	res = []
	for i in range(1, days_in_month+1):
		#print 'rem month',res
		res =find_actual_rem(data = res, day = i, month = month_default, year = year_default)
		#if rems:
		#	res.append(rems)
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
		print id_tuple
		cur.execute('SELECT textReminder, date_month, date_day, date_hour, date_minute from reminders where id = ?', id_tuple)
		data = cur.fetchone()
		#print 'all. step -', i, ' - ', data
		if data:			# if reminder had cut from database, this func return None. I control data for solving problems 
			res.append(data)
	con.close()
	#print res
	show_rem(name =u'All Reminders', data = res)

def control_env_fields(event):
	'''Control and if finds error - makes correctin of values in all Entry-fields.  (ent_year, ent_month, ent_day, ent_hour, ent_minute) 
	'''
	# TODO:	1. Make determination of curren weekday and find all remainders for this week in bd. - I am not sure that must do now
	#		2. Reminders for future and today must be signed with green color, for last - red!
	#show_status (u'Controll values in date-fields')
	month = ent_month.get()
	all_entry_fields = ((ent_year, year_default, year_default+10, year_default),  # consist of Entry (year, month, day, hour,minute), and determining values for min, max, default to everyone of it
	  					(ent_month, 1, 12, month_default),
	    				(ent_day, 1, days_in_month, day_default),
	     				(ent_hour, 0, 23, hour_default + 1),
	      				(ent_minute, 0, 59, minute_default))
	for field in all_entry_fields:
		#print field[0].get()
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
	# Fuction finds skiped reminders (creates a list), actual reminders (create a list) and next reminder
	# Data consist of:
	# [           0,          1,        2,         3,           4]
	# [textReminder, date_month, date_day, date_hour, date_minute]
	rem_actual_today = []
	rem_skiped_today = []
	# USE data from func refrash_date in the circle
	now = refrash_date()
	#hour_now = now[3]

	for rem in data:
		if rem[3]<hour_default:
			#print rem[3], ' < ', hour_default
			rem_skiped_today.append(rem)
		if rem[3] == now[3]:#hour_default:
			if rem[4] <= now[4]:#minute_default:
				rem_skiped_today.append(rem)
			if rem[4] > now[4]:#minute_default:
				rem_actual_today.append(rem)
		if rem[3] > now[3]:#hour_default:
			#print rem[3], ' > ', hour_default
			rem_actual_today.append(rem)
	if rem_actual_today:
		next_rem = rem_actual_today[0]
		show_rem(name = u'All actual Reminders for Today', data = rem_actual_today)
		#rem_actual_today.pop()
		
		print 'timer'
	else:
		next_rem = None
		showinfo(u'All actual Reminders for Today', u'No Reminder today')
	#print 'skip -', rem_skiped_today, len(rem_skiped_today)
	#print 'actual -', rem_actual_today, len(rem_actual_today)
	#print 'next -', next_rem
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
	# [           0,          1,        2,         3,           4]
	# [textReminder, date_month, date_day, date_hour, date_minute]
	now = refrash_date()
	hour_now = now[3]
	minute_now = now[4]

	if next_rem[4]>=minute_now:
		delta_seconds = ((next_rem[3] - hour_now)*60*60) + ((next_rem[4] - minute_now)*60)
		print '(', next_rem[3], '-', hour_now,') *3600 + (', next_rem[4], '-', minute_now,')*60 ===', delta_seconds 
	else:
		delta_seconds = ((next_rem[3] - hour_now)*60*60) - ((minute_now - next_rem[4])*60)
		print '(', next_rem[3], '-', hour_now,') *3600 - (', minute_now, '-', next_rem[4],')*60 ===', delta_seconds
	return delta_seconds

def show_message_treading():
	'''Function writes message in status window
	'''
	#status['text'] = 'Last operation: treading'
	print 'IT IS TIME TO DO: ', str(rem_actual[0][0])
	#rem_today(None) # message was written, find next message for today
	global show_done
	show_done = True
	print strftime("[%H:%M:%S]", gmtime()) + " show_done = ", show_done
	#print 'rem_actual was reduced until .pop() -->', rem_actual
	del rem_actual[0]
	print 'rem_actual was reduced with del -->', rem_actual
	if rem_actual:
		print 'in show_message_treading - call start_treading/ send -', rem_actual[0]
		delta_seconds_to_show = seconds_to_show_reminder(rem_actual[0]) # call seconds_to_show_reminder, wich return the nomber of seconds to show reminder
		start_treading(delta_seconds_to_show)

	

def start_treading(delta_seconds):
	'''TREADING FUNCTION - counts delta_seconds and then show Text of Reminder on screen
	'''
	global show_done
	print 'calling start_treading: show_done = ', show_done

	if show_done == True:
		timer = threading.Timer(delta_seconds, show_message_treading)
		timer.start()
		
		#print 'IN start_treading text glboal lists. Old:    ', rem_old 
		print 'IN start_treading text glboal lists. Actual: ', rem_actual
		show_done = False
		print strftime("[%H:%M:%S]", gmtime()) + " Start \n show_done = ", show_done
	else:
		print strftime("[%H:%M:%S]", gmtime()) + " NOT START"
	


########################################################################################################################

create_db()
#print sqlite3.version # currant version sqlite3
#print datetime.datetime.now().strftime("%d.%m.%Y.%I.%M.%p") # servicing info
#status_first = str(sqlite3.version) + '\n' + str(datetime.datetime.now().strftime("%d.%m.%Y.%I.%M.%p"))
print refrash_date()
print day_default, ' From refrash_date function'

# You can input your reminder in command line with format (after filename must be 6 arguments!):
# ...$ python rem_me.py 'MESSAGE' YEAR MONTH DAY HOUR MIN

if len(sys.argv)>1:
	reminder_from_cl(len(sys.argv))

###################################################################################################### Main window ####

root = Tk()
root.title(' My reminders')
root.minsize(height = 400, width = 620) # Min size of main window
root.maxsize(height = 400, width = 620) # Max size of main window

lab = Label(root, text = 'Write your reminder here:', font = 'Verdana 12')
lab.grid(row = 0, column = 0)

tx = Text(root, height = 6, width = 25, bg = 'lightgreen', font = "Verdana 14",	wrap = WORD) # textfield
tx.grid(row = 1, column = 0, sticky='nsew')

lab = Label(root, text = 'Write date:', font = 'Verdana 12')
lab.grid(row = 0, column = 1)

lab = Label(root, text = 'Year:', font = 'Verdana 10')
lab.grid(row = 2, column = 1)

w = Canvas(root, width = 220, height = 150)
w.create_line(0, 150, 220, 0, fill="red", dash=(4, 4))
w.create_text(22,12, text = 'HARM')
w.create_window(30,40) 									# not work!!!!
w.grid(row = 1, column = 1, columnspan = 2)

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

#but5 = Button(root)
#but5['text'] = "Cntrl fields"
#but5.bind('<Button-1>', control_env_fields)
#but5.grid(row = 8,  column = 0)

but6 = Button(root)
but6['text'] = "Rem ALL"
but6.bind('<Button-1>', reminder_all)
but6.grid(row = 8,  column = 1)

fra = Frame(root, height = 25, width = 400, bg = 'white') # as status window in the bootom of window
fra.grid(row = 9, column = 0)
status = Label(fra, text = 'Starting: '+ str(counter()) +' Reminders in DB \n Now: '
	+ str(datetime.datetime.now().strftime("%d.%m.%Y.%I.%M.%p")), font = 'Verdana 8', justify = 'left', bg = 'white')
status.grid(row = 0, column = 0)

#rem_actual = [['No actual remiders for today']]
#rem_old = [['NO old reminders for today']]
rem_today = reminder_today(None)
#if rem_today[1]:
#	rem_actual = rem_today[1]

#if rem_today[0]:
#	rem_old = rem_today[0]
#print 'rem today in main prog ',rem_today
#print 'rem today actual in main prog ', rem_actual
#print 'rem today old main prog ', rem_old

#while rem_actual:
#	show_done = False
#if rem_actual[0]:
#	text_next_message = rem_actual[0][0]
#else:
#	text_next_message = ' empty'
#print text_next_message
	#delta_seconds_to_show = seconds_to_show_reminder(rem_today[2][0])
	#start_treading(delta_seconds_to_show)
	
	#while True:
	#	if show_done: break
	#rem_actual.pop()


# [ next_rem,  rem_skiped_today,  rem_actual_today ]  
# [        0,               1[],               2[] ]               

#if rem_today[0]:

#	delta_seconds_to_show = seconds_to_show_reminder(rem_today[0])
#	start_treading(delta_seconds_to_show)

print 'There is:', counter(), 'records in database'
root.mainloop()