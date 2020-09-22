import paho.mqtt.client as mqtt
from Feedback import sensor_Data_Handler

# MQTT Settings 
MQTT_Broker = "test.mosquitto.org"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic = "MilkTemp/#"

#Subscribe to all Sensors at Base Topic
def on_connect(self, mosq, obj, rc):
	mqttc.subscribe(MQTT_Topic, 0)

#Save Data into DB Table
def on_message(mosq, obj, msg):

	print ("MQTT Data Received...")
	print ("MQTT Topic: " + msg.topic) 
	print ("Data: " + str(msg.payload))
	sensor_Data_Handler(msg.topic, msg.payload)


def on_subscribe(mosq, obj, mid, granted_qos):
    pass


mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe


# Connect
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))


# Continue the network loop
mqttc.loop_forever()
