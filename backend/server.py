#!/usr/bin/python
import sys
import time
import datetime
from Config import Config
from TaskScheduler import TaskScheduler
from Database import Database
from DataEngine import DataEngine, DataFetchFlags
from Exceptions import *



class WeatherServer():
	def __init__(self):
		pass
	
	def Start(self):
		print "---- Backend Server ----"
		
		#raise WAExceptionServer(WAExceptionServerTypes.StartError)
		
		# some comment
		# comment 2
		# comment q
		
		# hello 123
		
		engine = DataEngine()
		cond = engine.FetchData(0, DataFetchFlags.Conditions | DataFetchFlags.Alerts) 
		#print cond
		exit()
		
		
		if (cond == False):
			print "Site not found!"
			exit(1)
		
		print cond
		exit(0)
		"""
		d = {'Temperature': -3}
		db.StoreConditions(1, cond['CurrentConditions'])
		
		#Open IPC pipe
		#self.OpenPipe()
		"""
		#Initialize task scheduler
		self.Tasks = TaskScheduler()
		self.Tasks.LoadTasks()
		#exit()
		
		
		#Start loop
		self.MainLoop()
	
	def OpenPipe(self):
		try:
			self.ipcPipe = open(Config.Global.LcdPipeFile,"w")
		except:
			print "Error opening pipe!"
			exit(1)
		#Mark as open
		self.pipeOpen = True
		
	""" MAIN LOOP """		 
	def MainLoop(self):
		e = 1
		while (e == 1):
			time.sleep(.250)
			self.Tasks.DoEvents()
	
		
def main():
	server = WeatherServer()
	server.Start()
			
#Run main
if __name__ == '__main__':
	main()
