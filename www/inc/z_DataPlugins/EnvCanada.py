#!/usr/bin/python
from IDataProcessor import IDataProcessor
import urllib2
import xml.etree.ElementTree as ET
import sys
import helper
import json as json
from datetime import datetime
from bs4 import BeautifulSoup
sys.stderr = sys.stdout   

class DataProcessor(IDataProcessor):
	
	def __init__(self, processorParams):
		self._ProcessorParams = processorParams
		
	def _ExtractColumnData(self, dataIn):
		#Second Column - warnings
		ListItems = dataIn.find_all("li")
		ItemLinkUrl = None
		ItemType = None
		OutputItems = {}
		i = 0
		if (len(ListItems) > 0):
			for curItem in ListItems:
				ItemLinkUrl = curItem.a['href']
				#print ItemLinkUrl
				findId = ItemLinkUrl.split('#')[1]
				#print findId
				self._FetchAlertDetails("http://weather.gc.ca" + ItemLinkUrl, findId)
				ItemType =  curItem.a.string.__str__()
				OutputItems[i] = {'Type': ItemType, 'LinkUrl': ItemLinkUrl}
				OutputItems['count'] = i+1
				i += 1
		else:
			OutputItems['count'] = 0
		
		return OutputItems
	
	def FetchLocalAlerts(self, reportId):
		#print ""
		#Defaults to use if no data is returned
		outputData = {}
		outputData['counts' ] = {'warnings': 0, 'watches': 0, 'statements': 0}
		
		self.RemoteDataUrl = "http://weather.gc.ca/warnings/report_e.html?" + reportId
		#self.RemoteDataUrl = "http://weather.gc.ca/warnings/report_e.html?sk9"
		#self.RemoteDataUrl = "http://localhost/d/test-data-4.html"
		
		#Call the internal base class download content function, if it fails, return False
		if (self._DownloadContent() == False):
			return False
		
		#Get the raw data and read into an xml reader root
		html = self._RawDownloadedData
		
		#Soup it
		soup = BeautifulSoup(html.decode('utf-8','strict'))
		
		#Extract the name of the area
		dataFor = soup.html.main.find("h1", {'id': 'wb-cont', 'property': 'name'}).string.split(": ")[1]
		outputData['dataFor'] = dataFor
		
		#The base elements we will work with
		anchorElement = soup.html.main.find("div", {'class': 'col-xs-12'})
		
		#Catch no data, and return out
		if anchorElement.findAll(text='No Alerts in effect.'):
			return outputData
			
		
		#Counter
		i = 0
		
		#Content blank string
		_xContent = ""
		
		#Cycle thru all elements looking for data in the correct form
		for x in anchorElement:
			#Look for an H2, its content is the beginning of the warnings, watches, statements
			if (x.name == "h2"):
				currentType = x.string.__str__().lower()
				#Reset counter
				i = 0
				#Ready the new object
				outputData[currentType] = []
				_xContent = ""
				#print "=====" + currentType + "====="
				continue
			#Next item we want is a p.span
			elif (x.name == "p"):
				#Find the span: id and the date
				if (x.span != None):
					_xId = x.span['id']
					_xDateRaw = x.span.string
					#Let's fix the date into one we can work with
					#It appears in the format: h:mm [am/pm] timezone dayofweek day month year   
					#eg '3:22 PM EST Wednesday 19 November 2014'
					#print "-"
					#print _xDateRaw
					tempDate = _xDateRaw.split(" ")
					tempDate_Hr = int(tempDate[0].split(":")[0])
					tempDate_Min = int(tempDate[0].split(":")[1])
					tempDate_AmPm = tempDate[1]
					if (tempDate_AmPm == "PM"):
						if ((tempDate_Hr + 12) == 24):
							tempDate_Hr = 0
						else:
							tempDate_Hr += 12
					#tempDate_Tz = tempDate[2]
					tempDate_Day = int(tempDate[4])
					tempDate_Mon = int(datetime.strptime(tempDate[5],"%B").month)
					tempDate_Yr = int(tempDate[6])
					_xDate = datetime(tempDate_Yr, tempDate_Mon, tempDate_Day, tempDate_Hr, tempDate_Min, 0).strftime("%Y-%m-%dT%H:%M:%SZ")
					
					
					
					outputData[currentType].append({})
					outputData[currentType][i] = {'id': _xId, 'date': _xDate, 'disposition': None, 'title': None, 'contents': None, 'areas': None, 'caption': None }
					#continue
				#Inside the strong element is the title
				if (x.strong != None):
					#print x.strong
					_xTitle = x.strong.string.__str__()
					outputData[currentType][i]['title'] = _xTitle
					#Strip out the words 'in effect for:'
					if _xTitle.find(" in effect for:") != -1:
						_xDisposition = "InEffect"
						_xCaption = _xTitle.replace(" in effect for:", "").title()
					if _xTitle.find(" ended for:") !=-1 :
						_xDisposition = "Ended"
						_xCaption = _xTitle.replace(" ended for:", "").title()
						
					outputData[currentType][i]['disposition'] = _xDisposition
					outputData[currentType][i]['caption'] = _xCaption
				else:
					#It's just P elements, this contains the description data
					for contentChunk in x.contents:
						if (contentChunk.string != None):
							_xContent += contentChunk.string + " "
					#save the contents
					outputData[currentType][i]['contents'] = _xContent
					
			#Grab the UL list of the effected areas
			elif (x.name == "ul"):
				#Ignores the last UL item we dont need. It has no class associated with it so skip
				try:
					if x['class'] != None:
						continue
				except KeyError:
					pass
				
				#Once we get here, we know were looking at LI items
				listItems = x.find_all("li")
				areas = []
				#Cycle thru all items and put into array
				for item in listItems:
					areas.append(item.string)
				#Set it
				outputData[currentType][i]['areas'] = areas
				continue
				
			#if there is a DIV, it means there are more than one warning/statement/watch item in this group
			elif (x.name == "div"):
				#Inc counter
				i += 1
				#print "Item Count: " + str(i+1)
				continue
			else:
				pass

		#End of loop, now get counts
		try:
			warningCount = len(outputData['warnings'])
			outputData['counts']['warnings'] = warningCount
		except KeyError:
			pass
			
		try:
			watchCount = len(outputData['watches'])
			outputData['counts']['watches'] = watchCount
		except KeyError:
			pass
			
		try:
			statementCount = len(outputData['statements'])
			outputData['counts']['statements'] = statementCount
		except KeyError:
			pass
		
		#Return data
		return outputData


	
	def _FetchAlertDetails(self, url, toFind):
		self.RemoteDataUrl = url
		
		#Call the internal base class download content function, if it fails, return False
		if (self._DownloadContent() == False):
			return False
		
		#Get the raw data and read into an xml reader root
		html = self._RawDownloadedData
		
		#Soup it
		soup = BeautifulSoup(html.decode('utf-8','ignore'))
		
		anchorElement = soup.html.main.find("span", {'id': toFind})
		
		dataTime = anchorElement.string
		#todo: grab all location elements, if present???
		dataAlertText = anchorElement.parent.find("strong").string
		dataAlertFor = anchorElement.parent.parent.find("ul").li.string
		dataDetails = anchorElement.parent.parent.find_all("p")[1].contents
		print "-"
		print dataTime
		print dataAlertText
		print dataAlertFor
		print dataDetails
		#print "Hello"
		#print html
		
		return ""
		
		
	
	def FetchData(self):
		#Set where this data come from
		prov = self._ProcessorParams['ProvCode']
		city = self._ProcessorParams['CityCode']
		
		#formulate the correct remote URL from EC servers
		self.RemoteDataUrl = "http://dd.weatheroffice.gc.ca/citypage_weather/xml/%s/%s_e.xml" % (prov, city)
		
		#Call the internal base class download content function, if it fails, return False
		if (self._DownloadContent() == False):
			return False
		
		#Get the raw data and read into an xml reader root
		xmlRoot = ET.fromstring(self._RawDownloadedData)	
		
		#Conditions subelement
		curConds = xmlRoot.find('currentConditions')
		
		#Get station name
		valStation = curConds.find('station')
		self._CStationName = valStation.text
		
		#Get observation date/time, the second element set of dateTime (local time)
		valDT_Year = int(curConds.find('.dateTime[1]/year').text)
		valDT_Month = int(curConds.find('.dateTime[1]/month').text)
		valDT_Day = int(curConds.find('.dateTime[1]/day').text)
		valDT_Hour = int(curConds.find('.dateTime[1]/hour').text)
		valDT_Min = int(curConds.find('.dateTime[1]/minute').text)
		valDateTime = datetime(valDT_Year, valDT_Month, valDT_Day, valDT_Hour, valDT_Min, 0)
		self._CObservationDateTime = valDateTime.strftime("%Y-%m-%dT%H:%M:%SZ")
		
		#Get temperature
		valTemp = curConds.find('temperature')
		self._CTemperature = float(valTemp.text)
		
		#Get condition
		valCond = curConds.find('condition')
		if (valCond.text == None):
			self._CConditionType = "Clear"
		else:
			self._CConditionType = valCond.text
			
		#Get relative humidity
		valHumidity = curConds.find('relativeHumidity')
		self._CRelativeHumidity = float(valHumidity.text)
		
		#Get humidex, if present
		valHumidex = curConds.find('humidex')
		try:
			self._CHumidex = float(valHumidex.text)
		except AttributeError:
			self._CHumidex = None
			
		#Get dewpoint, if present
		valDewPoint = curConds.find('dewpoint')
		try:
			self._CDewPoint = float(valDewPoint.text)
		except AttributeError:
			self._CDewPoint = None
			
		#Get visiblity, if present
		valVisibility = curConds.find('visibility')
		try:
			self._CVisibility = float(valVisibility.text or -1)
		except AttributeError:
			self._CVisibility = -1
			
		#Get windchill, if present
		valWindChill = curConds.find('windChill')
		try:
			self._CWindChill = float(valWindChill.text)
		except AttributeError:
			self._CWindChill = None
			
		#Get baro pressure
		valPressure = curConds.find('pressure')
		self._CPressure = float(valPressure.text)
		if (valPressure.get('tendency') == "falling"):
			self._CPressureChange = -(float(valPressure.get('change') or 0))
		else:
			self._CPressureChange = (float(valPressure.get('change') or 0))
			
		#Get wind
		valWind = curConds.find('wind')
		valWindSpeed = valWind.find('speed')
		valWindDir = valWind.find('bearing')
		valWindGust = valWind.find('gust')
		self._CWindSpeed = float(valWindSpeed.text)
		self._CWindDirection = float(valWindDir.text or -1)
		self._CWindGust = float(valWindGust.text or -1)
		
	 	#Determine if windchill or humidex are present
		if (self._CWindChill != None) & (self._CHumidex == None):
			self._XFeels = self._CWindChill
		elif (self._CWindChill == None) & (self._CHumidex != None):
			self._XFeels = self._CHumidex
		else:
			self._XFeels = None
			
		
		
		
		
	
