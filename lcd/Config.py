""" ---- LCD Config File ----
"""
import sys

#Create config object used for the web site of things
class Config:
	GlobalConfigPath = "/home/mark/dev/weather"
	Global = None

#Add global config to this by loading it by adding it to the system path
sys.path.append(Config.GlobalConfigPath)  
from GlobalConfig import GlobalConfig
#Make it available locally
Config.Global = GlobalConfig()
