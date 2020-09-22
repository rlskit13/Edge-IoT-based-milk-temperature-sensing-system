import sqlite3

# SQLite DB Name
DB_Name =  "Milk_Tank_Temperature.db"

# SQLite DB Table Schema
TableSchema="""
drop table if exists Tank_1_Data ;
create table Tank_1_Data (
  id integer primary key autoincrement,
  SensorID text,
  Temperature float,
  Date_n_Time text
);


drop table if exists Tank_2_Data ;
create table Tank_2_Data (
  id integer primary key autoincrement,
  SensorID text,
  Temperature float,
  Date_n_Time text
);
"""

#Connect or Create DB File
conn = sqlite3.connect(DB_Name)
curs = conn.cursor()

#Create Tables
sqlite3.complete_statement(TableSchema)
curs.executescript(TableSchema)

#Close DB
curs.close()
conn.close()
