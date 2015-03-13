


class WAExceptionBase(Exception):
	def __init__(self, *dataParam):
		self.Desc = "Base"
		self.SubType = {'id': 0, 'desc': 'General error'}
		self.DataParam = dataParam
		
	def __str__(self):
		return repr("WeatherApplication." + self.Desc + ": " + (self.SubType['desc'] % self.DataParam) + " [" + str(self.SubType['id']) + "]")
		
		

class WAExceptionServerTypes():
	StartError = {'id': 100, 'desc': 'Error starting server'}
	PipeError = {'id': 101, 'desc': 'Error opening LCD communication pipe.'}
	
class WAExceptionServer(WAExceptionBase):
	def __init__(self, subType):
		self.Desc = "Server"
		self.SubType = subType
		

class WAExceptionDataEngineTypes():
	ModuleLoadError = {'id': 200, 'desc': 'Error loading module "%s"'}
	ModuleFuncCallFailure = {'id': 201, 'desc': 'An exception occured internally in module "%s" when calling function "%s"'}
	SiteNotFound = {'id': 210, 'desc': 'Data site #%s not found in collection'}
	SiteConfigInvalid = {'id': 211, 'desc': 'Data site #%s configuration invalid or missing parameters'}
	
	
	
class WAExceptionDataEngine(WAExceptionBase):
	def __init__(self, subType, *dataParam):
		self.Desc = "DataEngine"
		self.SubType = subType
		self.DataParam = dataParam



class WAExceptionDataPluginTypes():
	DownloadError = {'id': 300, 'desc': 'Error downloading data from remote site: "%s"'}
	DataParseError = {'id': 301, 'desc': 'Error parsing downloaded data from: "%s"'}
			
class WAExceptionDataPlugin(WAExceptionBase):
	def __init__(self, subType, *dataParam):
		self.Desc = "DataPlugin"
		self.SubType = subType
		self.DataParam = dataParam


class WAExceptionDatabaseTypes():
	ConnectionError = {'id': 400, 'desc': 'Error connecting to database: "%s"'}
	
			
class WAExceptionDatabase(WAExceptionBase):
	def __init__(self, subType, *dataParam):
		self.Desc = "Database"
		self.SubType = subType
		self.DataParam = dataParam
		
	
	
		
	

