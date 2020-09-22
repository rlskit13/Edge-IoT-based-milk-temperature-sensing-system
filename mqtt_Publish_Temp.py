import json
import time
import paho.mqtt.client as mqtt
import random, threading, json
from datetime import datetime

#====================================================
# MQTT Settings 
MQTT_Broker = "test.mosquitto.org"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic_Tank_1 = "MilkTemp/Tank_1"
MQTT_Topic_Tank_2 = "MilkTemp/Tank_2"
#====================================================
#MQTT Settings
def on_connect(client, userdata, rc):
	if rc != 0:
		pass
		print("Unable to connect to MQTT Broker...")
	else:
		print("Connected with MQTT Broker: ") + str(MQTT_Broker)

def on_publish(client, userdata, mid):
	pass
		
def on_disconnect(client, userdata, rc):
	if rc !=0:
		pass
		
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_publish = on_publish
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))		

#MQTT Publish message		
def publish_To_Topic(topic, message):
	mqttc.publish(topic,message)
	print ("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic))
	print ("")


def publish_reference_Sensor_Values_to_MQTT(SensorID):

	if SensorID == "Tank_1":
		Temp_Value = float("{0:.2f}".format(random.uniform(5, 10)))
		Tank_1_Data = {}
		Tank_1_Data['Sensor_ID'] = "Tank_1"
		Tank_1_Data['Data'] = Temp_Value
		Tank_1_Data['Date'] = (datetime.today()).strftime("%d-%b-%Y_%H:%M:%S:%f") 
		
		Tank_1_json_data = json.dumps(Tank_1_Data)

		print ("Publishing Tank 1 data: " + str(Temp_Value) + "...")
		publish_To_Topic (MQTT_Topic_Tank_1, Tank_1_json_data)


	elif SensorID == "Tank_2":
		Temp_Value = float("{0:.2f}".format(random.uniform(5, 10)))
		Tank_2_Data = {}
		Tank_2_Data['Sensor_ID'] = "Tank_2"
		Tank_2_Data['Data'] = Temp_Value
		Tank_2_Data['Date'] = (datetime.today()).strftime("%d-%b-%Y_%H:%M:%S:%f")

		Tank_2_json_data = json.dumps(Tank_2_Data)

		print ("Publishing Tank 2 data: " + str(Temp_Value) + "...")
		publish_To_Topic (MQTT_Topic_Tank_2, Tank_2_json_data)

	


if __name__ == '__main__':
	while True:
		publish_reference_Sensor_Values_to_MQTT("Tank_1")
		publish_reference_Sensor_Values_to_MQTT("Tank_2")
		time.sleep(300)
