#!/usr/bin/python
import cgi, cgitb
import json as json
import web
import sys
import importlib
from Config import Config
from helper import Validation

sys.stderr = sys.stdout      

http = web.Output()
http.Begin()
cfg = Config.Global

def main():
	#Define which functions to call based on the type input param
	ParamToFuncList = {	'test' : TestData,
						'conditions' : ReturnConditions
	}
	
	# Get the GET variables
	form = cgi.FieldStorage() 

	# Get data from fields
	paramType = form.getvalue('type')
	
	# Execute correct function based on param name, passing all the params into the function
	# BTW, I love this feature of Python where a list object's data can be called as a function!
	#try:
	data = ParamToFuncList[paramType] (form)
	#if not found, error out
	#except KeyError as e:
	#data =  {'status':'failure', 'errorMsg': 'Invalid type parameter.' } 
	
	
	
	#http.Print(json.dumps(data))
	http.Finish()

def TestData(formParams):
	#Get what site the data being requested
	getDataFor = (formParams.getvalue('for'))
	#http.Print("hello");
	#Grab the object from the config
	dataSiteConfig = cfg.DataSites[int(getDataFor)]
	
	#Look up the name of plugin to load to process this data
	processWithName = dataSiteConfig['ProcessWith']
	processorParams = dataSiteConfig['ProcessorParams']
	
	#Load the plugin, instanciating the object in the process with ()
	Plugin = _LoadPlugin(processWithName)(processorParams)
	#Plugin = DataProcessor()
	
	http.Print(Plugin.FetchLocalAlerts('on19'))
	
	
	
def ReturnConditions(formParams):
	#Get what site the data being requested
	getDataFor = (formParams.getvalue('for'))
	#http.Print("hello");
	#Grab the object from the config
	dataSiteConfig = cfg.DataSites[int(getDataFor)]
	
	#Look up the name of plugin to load to process this data
	processWithName = dataSiteConfig['ProcessWith']
	processorParams = dataSiteConfig['ProcessorParams']
	
	alertFilter = processorParams['AlertFilter']
	
	#Load the plugin, instanciating the object in the process with ()
	Plugin = _LoadPlugin(processWithName)(processorParams)
	#Plugin = DataProcessor()
	
	#Plugin.FetchAlerts()
	
	#Call fetch data method from plugin
	Plugin.FetchData()
	alertData = Plugin.FetchLocalAlerts(alertFilter)
	
	#Output the data as a JSON object
	conditionsData = Plugin.WeatherDataDict()
	data =  {'status':'success', 'caption': dataSiteConfig['Caption'], 'alerts': alertData, 'currentConditions': conditionsData }  
	
	#http.Print("aa")
	http.Print(json.dumps(data))
	
	#return "."

def _LoadPlugin(pluginName):
	#Formulate the correct class name to load
	full_class_string = "DataPlugins.%s.DataProcessor" % pluginName
	class_data = full_class_string.split(".")
	module_path = ".".join(class_data[:-1])
	class_str = class_data[-1]
	
	module = importlib.import_module(module_path)
	# Finally, we retrieve the Class
	return getattr(module, class_str)
	
#Run main
if __name__ == '__main__':
	main()
