import sqlite3
from Exceptions import WAExceptionDatabase, WAExceptionDatabaseTypes
import time
from Config import Config
import cPickle

class Database:
	def __init__(self):
		print "db - init"
		#connect to it
		dbFilename = Config.Global.Database['FilePath']
		self.IsConnected = False
		
		#Try to connect
		try:
			self.DbConnection = sqlite3.connect("/root/" +  dbFilename)
		except:
			print "Error opening database"
			raise WAExceptionDatabase(WAExceptionDatabaseTypes.ConnectionError, dbFilename)
			exit(1)
		
		#Grab cursor
		try:
			self.DbCursor = self.DbConnection.cursor()
		except:
			print "Error obtaining database cursor"
			exit(1)
		
		self.IsConnected = True
		
		#self.DbCursor.execute('SELECT * FROM current_conditions')
		#q = self.DbCursor.fetchone()
		#print q
		
	def StoreConditions(self, siteId, dataIn):
		lastUpdate = int(time.time())
		
		#Pickle incoming data
		pickledData = cPickle.dumps(dataIn)
		
		sql = """
			UPDATE current_conditions 
			SET
				last_update=:f_last_update,
				raw_data=:f_raw_data
			WHERE 
				site_id=:w_site_id
			"""
		
		#Map input data to correct fields
		t = {
			'w_site_id': siteId, 
			'f_last_update': lastUpdate,
			'f_raw_data': pickledData
		}	
		
		#Do the actual insert
		try:
			r = self.DbCursor.execute(sql, t)
			if (r.rowcount != 1):
				print "DB Insert Error - 1 row not inserted (site_id:", siteId, ")"
				return false
			self.DbConnection.commit()
		except Exception as e:
			self.DbConnection.rollback()
			print "DB Commit Error [" + e.__str__() + "]"
			#raise e
		finally:
			self.DbConnection.close()
		
		
		
	def __del__(self):
		#ensure db connection is closed
		self.DbConnection.close()
		
	
		
	
		
	


