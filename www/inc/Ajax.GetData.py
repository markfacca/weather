#!/usr/bin/python
import cgi, cgitb
import json as json
import web
import sys
import importlib
from Config import Config
from helper import Validation

sys.path.append(Config.BackendPath)  
from DataEngine import DataEngine, DataFetchFlags

sys.stderr = sys.stdout    
sys.tracebacklimit = 1  


http = web.Output()
http.Begin()
cfg = Config.Global
Engine = DataEngine()

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
	
	
	
	http.Finish()

def TestData(formParams):
	pass
	
def ReturnConditions(formParams):
	#Get what site the data being requested
	getDataFor = (formParams.getvalue('for'))
	
	#Grab data from data engine
	fetchFlags = DataFetchFlags.Conditions | DataFetchFlags.Alerts
	#fetchFlags = DataFetchFlags.Conditions
	dataRaw = Engine.FetchData(getDataFor, fetchFlags) 
	
	#Format it for JSON return
	dataOutput =  {'status':'success', 'caption': '_blank_', 'alerts': dataRaw['Alerts'], 'currentConditions': dataRaw['Conditions'] }  
	#Output as JSON
	http.Print(json.dumps(dataOutput))
	

#Run main
if __name__ == '__main__':
	main()
