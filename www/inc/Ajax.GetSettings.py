#!/usr/bin/python
import web
import json as json
from Config import Config

#Formulate data to return
outputData = {
	'RadarSites': Config.RadarSites,
	'DataSites': Config.Global.DataSites
}

#Serialize the output object into JSON and output, this it then loaded in javascript and parsed into an object
http = web.Output()
http.Begin()
http.Print(json.dumps(outputData))
http.Finish()

	
