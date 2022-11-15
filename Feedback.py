import json
import sqlite3

# SQLite DB Name
DB_Name =  "Milk_Tank_Temperature.db"

#===============================================================
# Database Manager Class



class DatabaseManager():
	def __init__(self):
		self.conn = sqlite3.connect(DB_Name)
		self.conn.execute('pragma foreign_keys = on')
		self.conn.commit()
		self.cur = self.conn.cursor()
		
	def add_del_update_db_record(self, sql_query, args=()):
		self.cur.execute(sql_query, args)
		self.conn.commit()
		return

	def __del__(self):
		self.cur.close()
		self.conn.close()


#===============================================================
# Functions to push Sensor Data into Database
# Function to save Temperature to DB Table
def Data_Handler(jsonData):
	
	#Parse Data 
	
	json_Dict = json.loads(jsonData)
	SensorID = json_Dict['Sensor_ID']
	Date_n_Time = json_Dict['Date']
	Temperature = json_Dict['Data']
	
	
	dbObj = DatabaseManager()
	
	dbObj.add_del_update_db_record(f"insert into {SensorID}_Data (SensorID, Temperature, Date_n_Time) values (?,?,?)",[SensorID, Temperature, Date_n_Time])
	
	del dbObj
	print (f"Inserted Temperature Data into {SensorID}.")
	#print ("")




#===============================================================
# Master Function to Select DB Funtion based on MQTT Topic

def sensor_Data_Handler(Topic, jsonData):

	Data_Handler(jsonData)

		
#===============================================================
