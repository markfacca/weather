import os
import sys
import cPickle

f = open("/var/tmp/lcd.ipc.pipe.read","w")


alertData = ['Tstorm Warning', 'Flood Watch']

c = {
	'ObservationDateTime': '2014-12-07T09:54:42Z', 
	'Temperature': -7, 
	'Feels': -14, 
	'Conditions': 'Light Rain', 
	'RelativeHumidity': 37, 
	'Pressure': 100.2, 
	'PressureChange': -0.12, 
	'WindSpeed': 21, 
	'WindDirection': 56, 
	'WindGust': 61,
	'AlertsPresent': False,
	'AlertData': alertData}


cPickle.dump(c,f)

#f.write(s)
f.close()
