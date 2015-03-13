from Task import Task
import time
from datetime import datetime



"""	TaskClock
	Executes a task at a specific clock time with wildcards if needed.
	
	@inherits	Task
"""
class TaskClock(Task):
	TaskType = "Clock"
	""" Constructor
		TaskClock constructor
	
		@param 	taskName			String name of task
		@param 	functionToRun		Object that gets called when the task runs
		@param 	functionParams		Dict of params to pass to the task when run
		@param	hourPart			Hour or "*" for wildcard
		@param	minutePart			Minute or "*" for wildcard
		@param	secondPart			Second or "*" for wildcard
		@return 					na
	"""
	def __init__(self, taskName, functionToRun, functionParams, hourPart, minutePart, secondPart):
		#Call the base class ctor first
		super(TaskClock, self).__init__(taskName, functionToRun, functionParams)
		#Add specific stuff
		self._hourPart = hourPart
		self._minutePart = minutePart
		self._secondPart = secondPart
		self._lastRanAtClock = None
		
	def DetailsToString(self):
		return "HourPart={0}, MinutePart={1}, SecondPart={2}".format(self._hourPart, self._minutePart, self._secondPart)
		
	""" CheckTimer
		Checks to see if the task should run based on the current clock time.
		
		@override
		@param						na
		@return 					na
	"""
	def CheckTimer(self):
		#Make sure we don't run the same event multiple times for a given time interval
		#This can happen if the CheckTimer is called multiple times in less than 1 second as this
		#is our shortest interval.
		if datetime.now().strftime("%H%M%S") == self._lastRanAtClock:
			#print "already ran once"
			return
			
		
		clockHour = datetime.now().hour
		clockMinute = datetime.now().minute
		clockSecond = datetime.now().second
		
		hourGood = False
		minuteGood = False
		secondGood = False
		
		if (self._hourPart == "*"):
			hourGood = True
		elif int(clockHour) == int(self._hourPart):
			hourGood = True
		
		if (self._minutePart == "*"):
			minuteGood = True
		elif int(clockMinute) == int(self._minutePart):
			minuteGood = True
			
		if (self._secondPart == "*"):
			secondGood = True
		elif int(clockSecond) == int(self._secondPart):
			secondGood = True
		
		#Once all items have been verified as true, log and run task
		if ((hourGood == True) & (minuteGood == True) & (secondGood == True)):
			self._lastRanAtClock = datetime.now().strftime("%H%M%S")
			self.RunTask()
		
			
