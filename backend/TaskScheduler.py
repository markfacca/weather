import os
from Config import Config
from glob import glob
import importlib
#from TaskDefs import TaskDefs
#from TaskPlugins.EnvCanada import CustomTask as CustomTask1


"""	TaskScheduler
	Takes care of loading, and executing the events.
	
	
	@inherits	na
"""
class TaskScheduler():
	"""	Constructor
	
		@params				na
		@return				na
	"""
	def __init__(self):
		self.Tasks = []
		
	"""	LoadTasks
		Loads the tasks objects dynamically into an array
	
		@params				na
		@return				na
	"""
	def LoadTasks(self):
		#Load all plugins from the TaskPlugin folder, with the name *.Task.py
		fileList = glob("./TaskPlugins/*.py")
		
		
		for i in fileList:
			modName = (i.split("/")[-1]).split(".")[0]
			if (modName != "__init__"):
				print "Loading tasks module %s..." % modName,
				mod = self._LoadModule(modName)()
				if (mod.PluginType == "Task"):
					print "success"
					self.Tasks.append(mod)
				else:
					print "failure"
		

		
	
	def _LoadModule(self, moduleName):
		#Formulate the correct class name to load
		full_class_string = "TaskPlugins.%s.CustomTask" % moduleName
		class_data = full_class_string.split(".")
		module_path = ".".join(class_data[:-1])
		class_str = class_data[-1]
		
		module = importlib.import_module(module_path)
		# Finally, we retrieve the class returning it as an object
		return getattr(module, class_str)


	"""	DoEvents
		Gets called from the main server event loop at a regular interval. Cycles
		through each task, and executes CheckTimer to see if the task needs to run.
	
		@params				na
		@return				na
	"""
	def DoEvents(self):
		for curTask in self.Tasks:
			if (curTask._lastError == None):
				curTask.CheckTimer()
			
			#print curTask._lastError
			
