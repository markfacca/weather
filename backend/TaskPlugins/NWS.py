from base.TaskInterval import TaskInterval
from DataEngine import DataEngine
from DataFetchFlags import DataFetchFlags
from Database import Database
import pickle

"""	CustomTask -
	Fetches Environment Canada conditions at a regular interval
	
	@inherits	TaskClock
"""
class CustomTask(TaskInterval):
	
	"""	Constructor
		Initialize the task, filling in the necessary default parameters for the type of task, then call its base ctor.
		
		@params				na
		@return				na
	"""
	def __init__(self):
		#Call super filling in required params
		super(CustomTask, self).__init__(taskName="NWS", functionToRun=self._InternalRunTask, functionParams={"hello"}, interval=10)
	
	""" _InternalRunTask
		Function, as specified by _functionToRun, that gets called externally by the base class function RunTask as a new thread
		This is where the unique logic and code is placed.
		
		@param	*kwargs		Variable number of arguments passed to the function from the TaskScheduler when called. 
	"""
	def _InternalRunTask(self, *kwargs):
		engine = DataEngine()
		cond = engine.FetchData(0, DataFetchFlags.Conditions)
		
		
		print cond
		print "National Weather Service fetching..."
		print kwargs
		#raise Exception
		pass
