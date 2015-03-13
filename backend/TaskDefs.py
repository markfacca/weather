import sys
from Task import Task
from TaskInterval import TaskInterval
from TaskClock import TaskClock

class TaskDefs:
	Tasks = {
		0: TaskInterval("CheckConditions", None, {None}, 30)
		}	
		
		
