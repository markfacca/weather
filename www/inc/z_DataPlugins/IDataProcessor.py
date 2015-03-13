#!/usr/bin/python
import urllib2
import xml.etree.ElementTree as ET


#
# Base object for fetching data
#

class IDataProcessor:
	RemoteDataUrl = "[unset]"
	_RawDownloadedData = ""
	_CStationName = None
	_CObservationDateTime = None
	_CTemperature = None;
	_CConditionType = None
	_CRelativeHumidity = None
	_CHumidex = None
	_CWindChill = None
	_CPressure = None
	_CPressureChange = None
	_CWindSpeed = None
	_CWindDirection = None
	_CWindGust = None
	_CDewPoint = None
	_CVisibility = None
	_XFeels = None
	
	def About(self):
		print ""
	
	
	def __init__(self):
		#print "INIT"
		pass
		
	def FetchData(self):
		pass
		
	def StationName(self):
		return self._CStationName
		
	def ObservationDateTime(self):
		return self._CObservationDateTime	
	
	def Temperature(self):
		return self._CTemperature
		
	def RelativeHumidity(self):
		return self._CRelativeHumidity
		
	def Humidex(self):
		return self._CHumidex
		
	def WindChill(self):
		return self._CWindChill
	
	def ConditionType(self):
		return self._CConditionType
		
	def Pressure(self):
		return self._CPressure
		
	def PressureChange(self):
		return self._CPressureChange
		
	def WindSpeed(self):
		return self._CWindSpeed
		
	def WindDirection(self):
		return self._CWindDirection
		
	def WindGust(self):
		return self._CWindGust
		
	def DewPoint(self):
		return self._CDewPoint
		
	def Visibility(self):
		return self._CVisibility
		
	def Feels(self):
		return self._XFeels
		
	def WeatherDataDict(self):
		output = {}
		output['StationName'] = self.StationName()
		output['ObservationDateTime'] = self.ObservationDateTime()
		output['Temperature'] = self.Temperature()
		output['RelativeHumidity'] = self.RelativeHumidity()
		output['Humidex'] = self.Humidex()
		output['WindChill'] = self.WindChill()
		output['Conditions'] = self.ConditionType()
		output['Pressure'] = self.Pressure()
		output['PressureChange'] = self.PressureChange()
		output['WindSpeed'] = self.WindSpeed()
		output['WindDirection'] = self.WindDirection()
		output['WindGust'] = self.WindGust()
		output['DewPoint'] = self.DewPoint()
		output['Visibility'] = self.Visibility()
		output['Feels'] = self.Feels()
		return output
		
	def __str__(self):
		return ""
		pass
		
		
	def _DownloadContent(self):
		try:
			response = urllib2.urlopen(self.RemoteDataUrl)
		except urllib2.HTTPError:
			return False
			
		#Get response and read into variable
		self._RawDownloadedData = response.read()
	

	
	
		
		
		
		
		
	
	
