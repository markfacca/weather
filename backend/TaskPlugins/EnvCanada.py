from base.TaskClock import TaskClock


"""	CustomTask -
	Fetches Environment Canada conditions at a regular interval
	
	@inherits	TaskClock
"""
class CustomTask(TaskClock):
	"""	Constructor
		Initialize the task, filling in the necessary default parameters for the type of task, then call its base ctor.
		
		@params				na
		@return				na
	"""
	def __init__(self):
		#Call super filling in required params
		super(CustomTask, self).__init__(taskName="EnvCanada 1", functionToRun=self._InternalRunTask, functionParams={"hello"}, hourPart="*", minutePart=11, secondPart=0)
	
	""" _InternalRunTask
		Function, as specified by _functionToRun, that gets called externally by the base class function RunTask as a new thread
		This is where the unique logic and code is placed.
		
		@param	*kwargs		Variable number of arguments passed to the function from the TaskScheduler when called. 
	"""
	def _InternalRunTask(self, *kwargs):
		print DataFetchFlags.Alerts
		print "EnvCanada fetch..."
		print kwargs
		try:
			raise Exception
		except:
			pass
		finally:
			self._lastError = "oops"
		pass
