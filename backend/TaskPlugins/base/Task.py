# Task.py
# 
# Task base object which everything else inherits from.
# 
import time
import datetime
import threading

"""	Task
	The base class for tasks
	
	@inherits	object
"""
class Task(object):
	PluginType = "Task"
	TaskType = "Base"
	
	""" Constructor
		Base class constructor
	
		@param 	taskName			String name of task
		@param 	functionToRun		Object that gets called when the task runs
		@param 	functionParams		Dict of params to pass to the task when run
		@return 					na
	"""
	def __init__(self, taskName, functionToRun, functionParams):
		self._taskName = taskName
		self._functionToRun = functionToRun
		self._functionParams = functionParams
		#self._lastRanAt = time.time()
		self._lastRanAt = None
		self._lastError = None
		
	def About(self):
		return "Base task module"
		
	def __repr__(self):
		return "<Task Type={0}, Name={1}, LastRun={2}, {3}>".format(self.TaskType, self._taskName, self._lastRanAt, self.DetailsToString())
	
	def DetailsToString(self):
		return None
		
	""" CheckTimer
		Called by the task scheduler on a regular basis (in a loop) to determine if the task should run.
	
		Is overridden by child classes to implement scheduling logic
		@param						na
		@return 					na
	"""
	def CheckTimer(self):
		#This is where the logic for a type of task would go. For example,
		#a task could occur at a specific interval, or at a specific real clock time
		
		#For the base class, just run it, don't do anything else
		
		self.RunTask()
		
			

		
	""" RunTask
		Called by CheckTimer when the task is run. Spawns a new thread to run the task function, 
		logging the timestamp the task was started (not completed).
		
		Typically not overridden
		@param						na
		@return 					na
	"""
	def RunTask(self):
		print "+- Run Task " + ("-" * 50) + "+"
		print "Name: " + self._taskName
		#Create new thread to run 
		workerThread = threading.Thread(target=self._functionToRun, args=(self._functionParams))
		workerThread.name = "Thread_" + self._taskName
		workerThread.start()
		self._lastRanAt = time.time()

	
