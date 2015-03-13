#!/usr/bin/python
import web
import json as json

class Config:

	def __init__(self):
		"""self.RadarSites = {
			0: {"Caption": "Burlington - Local", "Url": "http://radblast.wunderground.com/cgi-bin/radar/WUNIDS_composite?centerlat=43.33.2&centerlon=-79.82&radius=14&type=N0R&num=1&delay=50&width=[w]&height=[h]&newmaps=1&smooth=1&showstorms=0&showlabels=1&lightning=1&brand=mobile"},
			1: {"Caption": "Burlington - Wide", "Url": "http://radblast.wunderground.com/cgi-bin/radar/WUNIDS_composite?centerlat=43.33.2&centerlon=-79.82&radius=60&type=N0R&num=1&delay=50&width=[w]&height=[h]&newmaps=1&smooth=1&showstorms=0&showlabels=1&lightning=1&brand=mobile"},
			2: {"Caption": "Burlington - Wide (Loop, Storms)", "Url": "http://radblast.wunderground.com/cgi-bin/radar/WUNIDS_composite?centerlat=43.33.2&centerlon=-79.82&radius=60&type=N0R&num=5&delay=30&width=[w]&height=[h]&newmaps=1&smooth=1&showstorms=1&showlabels=1&lightning=1&brand=mobile"}
		}"""
		self.DataSites = {
			0: {"Caption": "Hamilton (EC)", "ProcessWith": 'EnvCanada', "ProcessorParams": {"ProvCode": "ON", "CityCode": "s0000549", "AlertFilter": "on58"}},
			1: {"Caption": "Sarnia (EC)", "ProcessWith": 'EnvCanada', "ProcessorParams": {"ProvCode": "ON", "CityCode": "s0000796", "AlertFilter":"on36"}},
			2: {"Caption": "Burlington - Palmer (PWS)", "ProcessWith": 'PWS', "ProcessorParams": {"Station": "IONTARIO343"}},
			3: {"Caption": "Test 2 ", "ProcessWith": 'EnvCanada', "ProcessorParams": {"ProvCode": "NU", "CityCode": "s0000065", "AlertFilter": "on19"}},
			4: {"Caption": "Toronto (EC)", "ProcessWith": 'EnvCanada', "ProcessorParams": {"ProvCode": "ON", "CityCode": "s0000458"}}
		}
		
if __name__ == '__main__':
	#Serialize the config object into JSON and output, this it then loaded in javascript and parsed into an object
	cfg = Config()
	http = web.Output()
	http.Begin()
	http.Print(json.dumps(cfg.__dict__))
	http.Finish()

	
