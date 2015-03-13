from Config import Config
from Exceptions import WAExceptionDataEngine, WAExceptionDataEngineTypes
from Database import Database
from DataFetchFlags import DataFetchFlags
import importlib

	
class DataEngine:
	def __init__(self):
		pass
	
	def Test123(self):
		print "Test123"
		
	def FetchData(self, forSite, flags):
		outputData = {}
		
		#Grab the current data site info from config
		try:
			currentDataSite = Config.Global.DataSites[int(forSite)]
		except KeyError:
			raise WAExceptionDataEngine(WAExceptionDataEngineTypes.SiteNotFound, forSite)
			return false
		try:
			moduleName = currentDataSite['ProcessWith']
			processorParams = currentDataSite['ProcessorParams']
		except KeyError: 
			raise WAExceptionDataEngine(WAExceptionDataEngineTypes.SiteConfigInvalid, forSite)
			
		#Load module, passing in the processor params to it on init
		try:
			Module = self._LoadModule(moduleName)(processorParams)
		except:
			raise WAExceptionDataEngine(WAExceptionDataEngineTypes.ModuleLoadError, moduleName)
		
		#Fetch new data based on flags
		if (flags & DataFetchFlags.Conditions):
			try:
				#Do data fetch
				Module.FetchConditions()
				
				#Store data in DB unless set not to 
				rawData = Module.ReturnConditions()
				if not (flags & DataFetchFlags.NoDbUpdate):
					db = Database()
					db.StoreConditions(forSite, rawData)
					
				#Return data
				outputData['Conditions'] = Module.ReturnConditions()
			except Exception as e:
				#raise WAExceptionDataEngine(WAExceptionDataEngineTypes.ModuleFuncCallFailure, moduleName, "FetchConditions")
				raise e
	
		if (flags & DataFetchFlags.Alerts):
			try:
				Module.FetchAlerts()
				outputData['Alerts'] = Module.ReturnAlerts()
			except:
				raise WAExceptionDataEngine(WAExceptionDataEngineTypes.ModuleFuncCallFailure, moduleName, "FetchAlerts")
		
		#Return all of it
		return outputData
		
		
		
		
	def _LoadModule(self, moduleName):
		#Formulate the correct class name to load
		full_class_string = "DataPlugins.%s.DataProcessor" % moduleName
		class_data = full_class_string.split(".")
		module_path = ".".join(class_data[:-1])
		class_str = class_data[-1]
		
		module = importlib.import_module(module_path)
		# Finally, we retrieve the class
		return getattr(module, class_str)
