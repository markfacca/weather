#!/usr/bin/python
from lcd_driver import LCD
from Config import Config
import datetime
import time
import thread
import os
import cPickle



class Application:
	#Grab IPC pipe filename from global config
	pipeFilename = Config.Global.LcdPipeFile
	#Define some default valus
	displayStateDurations = [45,15]
	displayStateShowAlerts = False
	alertsPresent = False
	
	currentConditions =  {
		'Time':				'##:##',
		'Temperature':		'#', 
		'Feels':			'#',
		'Conditions':		'#',
		'PressureAndChange':'#',
		'WindAndDir': 		'#',
		'WindGust': 		'#',
		'RelativeHumidity': '#',
		'AlertData':		['', '', '']
	}
	#Symbols used for the controller
	SYM_DEG = chr(128)
	SYM_UP = chr(222)
	SYM_DOWN = chr(224)
	SYM_LEFT = chr(223)
	
	#Ctor
	def __init__(self):
		pass
		
	#Open serial port and initialize things
	def Startup(self):
		#Instantiate LCD controller object
		self.lcdDisplay = LCD()
		#Connect to it
		self.lcdDisplay.Connect("/dev/ttyUSB0")
		
		#Init LCD into a known, good state
		self.lcdDisplay.InitialSetup()
		self.lcdDisplay.ClearScreen()
		#Update initial data, which is no data
		self.UpdateDisplay()
		#Open/create the IPC pipe
		self.OpenPipe()
		#Start the main loop
		self.MainLoop()
		
	def OpenPipe(self):
		#Open a name pipe in 
		try:
			os.mkfifo(self.pipeFilename)
		except:
			print "Pipe " + self.pipeFilename + " already exists!"
		
		#Open the pipe
		try:
			print "Opening pipe..."
			self.ipcReadFile = open(self.pipeFilename, "r")
			
		except:
			print "Error opening the pipe"
			exit(1)
		print "Pipe open!"
	
	def MainLoop(self):
		#Infine loop
		e = 1
		timeElapsed = time.time()
		# ---- START MAIN LOOP ----	
		while (e == 1):
			#Non block read
			dataIn = self.ipcReadFile.read()
			
			#Check if not zero, then read
			if (len(dataIn) > 0):
				ipcObject = cPickle.loads(dataIn)
				#Format raw data into current state objects
				self.FormatData(ipcObject)
				
				#Check if alerts are present, if not ensure it's hidden and not stuck
				if (self.alertsPresent == False):
					self.displayStateShowAlerts = False
				else:
					self.displayStateShowAlerts = True
					
				#Update the change
				self.UpdateDisplay()
			
			#If alerts are present, cycle thru the regular conditions and alerts screen
			if (self.alertsPresent == True):
				if (self.displayStateShowAlerts == False):
					#We're timing the regular screen duration
					if (time.time() > (timeElapsed + self.displayStateDurations[0])):
						self.displayStateShowAlerts = True
						timeElapsed = time.time()
						self.UpdateDisplay()
				else:
					if (time.time() > (timeElapsed + self.displayStateDurations[1])):
						self.displayStateShowAlerts = False
						timeElapsed = time.time()
						self.UpdateDisplay()
						
			#Sleep for 100ms. If this isn't done the CPU shoots up to 100% usage!
			time.sleep(0.1)
				
		# ---- END MAIN LOOP ----
			
			
	
	def FormatData(self, inputObject):
		#Format all incoming raw data accordingly
		
		#Format easy stuff
		self.currentConditions['Conditions'] = str(self._CheckIfMissing(inputObject, 'Conditions', '-'))[:20]
		self.currentConditions['Temperature'] = str(self._CheckIfMissing(inputObject, 'Temperature', '-'))
		self.currentConditions['Feels'] = str(self._CheckIfMissing(inputObject, 'Feels', '-'))
		self.currentConditions['RelativeHumidity'] = str(self._CheckIfMissing(inputObject, 'RelativeHumidity', '-'))
		
		#Format observation time
		self.currentConditions['Time'] = inputObject['ObservationDateTime'][11:16]
		
		#Format pressure
		pressureValueString = str(self._CheckIfMissing(inputObject, 'Pressure', '-'))
		pressureChange = self._CheckIfMissing(inputObject, 'PressureChange', None)
		
		#Change pressure changes into up/down characters
		if (pressureChange != None):
			if (pressureChange < 0):
				pressureChangeString = self.SYM_DOWN
			elif (pressureChange > 0):
				pressureChangeString = self.SYM_UP
			elif (pressureChange == 0):
				pressureChangeString = " "
		else:
			pressureChangeString = "-"
				
		self.currentConditions['PressureAndChange'] = pressureValueString + pressureChangeString
		
		#Format wind
		windValueString = str(self._CheckIfMissing(inputObject, 'WindSpeed', '-'))
		windDirString = self._ToCardinalDir(self._CheckIfMissing(inputObject, 'WindDirection', None))
		windGustString = str(self._CheckIfMissing(inputObject, 'WindGust', '-'))
		self.currentConditions['WindAndDir'] = windValueString + " " + windDirString
		self.currentConditions['WindGust'] = windGustString 
		
		#Are alerts present
		self.alertsPresent = inputObject['AlertsPresent']
		
		#Only take top three alerts - for now
		i = 0
		for alertText in inputObject['AlertData'][0:3]:
			self.currentConditions['AlertData'][i] = self.SYM_LEFT + alertText
			i += 1
		
		
		
	def _CheckIfMissing(self, inputObject, key, defaultValue):
		try:
			outValue = inputObject[key]
		except KeyError:
			outValue = defaultValue
			
		return outValue
	
	def _ToCardinalDir(self, angleParam):
		angle = angleParam
		if ((angle >= 337.5) & (angle <= 360)):
			return "N"
		elif ((angle >= 0) & (angle < 22.5)):
			return "N"
		elif ((angle > 22.5) & (angle < 67.5)):
			return "NE"
		elif ((angle >= 67.5) & (angle <= 112.5)):
			return "E"
		elif ((angle > 112.5) & (angle < 157.5)):
			return "SE"
		elif ((angle >= 157.5) & (angle <= 202.5)):
			return "S"
		elif ((angle > 202.5) & (angle < 247.5)):
			return "SW"
		elif ((angle >= 247.5) & (angle <= 292.5)):
			return "W"
		elif ((angle > 292.5) & (angle < 337.5)):
			return "NW"
		else:
			return "#"
		
	
	def UpdateDisplay(self):
		if (self.displayStateShowAlerts == False):
			self.lcdDisplay.ClearScreen()
			self.lcdDisplay.WriteString(15,0, self.currentConditions['Time'])
			self.lcdDisplay.WriteString(0,0, self.currentConditions['Conditions'])
			self.lcdDisplay.WriteString(0,1,"T:" + self.currentConditions['Temperature'] + self.SYM_DEG + "C")
			self.lcdDisplay.WriteString(11,1,"F:" + self.currentConditions['Feels'])
			self.lcdDisplay.WriteString(0,2,"B:" + self.currentConditions['PressureAndChange'])
			self.lcdDisplay.WriteString(11,2,"RH:" + self.currentConditions['RelativeHumidity'] + "%")
			self.lcdDisplay.WriteString(0,3,"W:" + self.currentConditions['WindAndDir'])
			self.lcdDisplay.WriteString(11,3,"WG:" + self.currentConditions['WindGust'])
		else:
			self.lcdDisplay.ClearScreen()
			self.lcdDisplay.WriteString(0,0, "ALERTS!")
			self.lcdDisplay.WriteString(0,1, self.currentConditions['AlertData'][0])
			self.lcdDisplay.WriteString(0,2, self.currentConditions['AlertData'][1])
			self.lcdDisplay.WriteString(0,3, self.currentConditions['AlertData'][2])



def main():
	app = Application()
	app.Startup()
	
	
		
#Run main
if __name__ == '__main__':
	main()
