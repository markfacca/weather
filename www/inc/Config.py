""" ---- Web Frontend Config File ----
"""
import sys

#Create config object used for the web site of things
class Config:
	BackendPath = "/home/mark/dev/weather/backend"
	GlobalConfigPath = "/home/mark/dev/weather"
	RadarSites = {
		0: {"Caption": "Burlington - Local", "Url": "http://radblast.wunderground.com/cgi-bin/radar/WUNIDS_composite?centerlat=43.33.2&centerlon=-79.82&radius=14&type=N0R&num=1&delay=50&width=[w]&height=[h]&newmaps=1&smooth=1&showstorms=0&showlabels=1&lightning=1&brand=mobile&rainsnow=1"},
		1: {"Caption": "Burlington - Wide", "Url": "http://radblast.wunderground.com/cgi-bin/radar/WUNIDS_composite?centerlat=43.33.2&centerlon=-79.82&radius=60&type=N0R&num=1&delay=50&width=[w]&height=[h]&newmaps=1&smooth=1&showstorms=0&showlabels=1&lightning=1&brand=mobile&rainsnow=1"},
		2: {"Caption": "Burlington - Wide (Loop, Storms)", "Url": "http://radblast.wunderground.com/cgi-bin/radar/WUNIDS_composite?centerlat=43.33.2&centerlon=-79.82&radius=60&type=N0R&num=5&delay=30&width=[w]&height=[h]&newmaps=1&smooth=1&showstorms=1&showlabels=1&lightning=1&brand=mobile&rainsnow=1"}
	}
	Global = None

#Add global config to this by loading it by adding it to the system path
sys.path.append(Config.GlobalConfigPath)  
from GlobalConfig import GlobalConfig
#Make it available locally
Config.Global = GlobalConfig()
