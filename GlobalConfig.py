""" ---- Global Config ----
Global configuration file for all elements of the weather system
Used and loaded in each local Config.py file for:
	- Web interface frontend in www/
	- Backend server in backend/
	- LCD server in lcd/
"""
class GlobalConfig:
	DataSites = {
			0: {"Caption": "Hamilton (EC)", "ProcessWith": 'EnvCanada', "ProcessorParams": {"ProvCode": "ON", "CityCode": "s0000549", "AlertFilter": "on58"}},
			1: {"Caption": "Sarnia (EC)", "ProcessWith": 'EnvCanada', "ProcessorParams": {"ProvCode": "ON", "CityCode": "s0000796", "AlertFilter":"on36"}},
			2: {"Caption": "Burlington - Palmer (PWS)", "ProcessWith": 'PWS', "ProcessorParams": {"Station": "IONTARIO343"}},
			3: {"Caption": "Test 2 ", "ProcessWith": 'EnvCanada', "ProcessorParams": {"ProvCode": "NU", "CityCode": "s0000065", "AlertFilter": "nb14"}},
			4: {"Caption": "Toronto (EC)", "ProcessWith": 'EnvCanada', "ProcessorParams": {"ProvCode": "ON", "CityCode": "s0000458", "AlertFilter": "on61"}}
	}
	LcdPipeFile = "/var/tmp/lcdserver.pipe"
	Database = {
			"FilePath": "../db/weather.db"
	}
	
