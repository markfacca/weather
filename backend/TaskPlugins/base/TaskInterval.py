from Task import Task
import time

"""	TaskInterval
	Executes a task at a specific interval.
	
	@inherits	Task
"""
class TaskInterval(Task):
	TaskType = "Interval"
	""" Constructor
		TaskInterval constructor
	
		@param 	taskName			String name of task
		@param 	functionToRun		Object that gets called when the task runs
		@param 	functionParams		Dict of params to pass to the task when run
		@param	interval			Interval in seconds this task should run
		
		@return 					na
	"""
	def __init__(self, taskName, functionToRun, functionParams, interval):
		#Call the base class ctor first
		super(TaskInterval, self).__init__(taskName, functionToRun, functionParams)
		#Add specific stuff
		self._interval = interval
		
	def DetailsToString(self):
		return "Interval={0}".format(self._interval)
		
		
	""" CheckTimer
		Checks to see if the task should run based on how many seconds have elapsed since it last run.
		
		@override
		@param						na
		@return 					na
	"""	
	def CheckTimer(self):
		#First check to see if the task has run the first time or not
		if self._lastRanAt == None:
			self.RunTask()
		
		#Check if timer + interval has elapsed since last time
		currentTimer = time.time()
		compareTimer = self._lastRanAt + self._interval
		
		#Check if it's time to run task
		if (currentTimer >= compareTimer):
			#Run it
			self.RunTask()
		
			
