from Config import Config

class TaskScheduler():
	def __init__(self):
		self._taskItems = []
	
	#Add a task	
	def AddTask(self, task):
		self._taskItems.append(task)
	
	#Cycle thru all events doing a check/run on them
	def DoEvents(self):
		for curTask in self._taskItems:
			curTask.CheckTimer()
