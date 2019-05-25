"""
simple test - python3 anf paho.mqtt library

"""

import time, requests, json, math
#https://mntolia.com/mqtt-python-with-paho-mqtt-client/
import paho.mqtt.client as mqtt


def read_mqtt_config():
    # TODO file does not exist
    f = open('config/mqtt.json', 'r')
    d = f.read()
    f.close()
    return json.loads(d)    

#the callback function
def on_connect(client, userdata, flags, rc):
     print("Connected With Result Code {}".format(rc))
     client.subscribe("TestingTopic")

def on_disconnect(client, userdata, rc):
	print("Disconnected From Broker")

def on_message(client, userdata, message):
	print(message.payload.decode())
	print(message.topic)

def on_publish(client, userdata, mid):
	print("mid:{}".format(mid))

print("read_mqtt_config >")
mqtt_clientid_prefix = read_mqtt_config()["mqtt_clientid_prefix"]
mqtt_host = read_mqtt_config()["mqtt_broker_ip"]
mqtt_port = read_mqtt_config()["mqtt_port"]
mqtt_root_topic = read_mqtt_config()["mqtt_root_topic"]
#mqtt_ssl  = False # Consider to use TLS!
mqtt_ssl  = read_mqtt_config()["mqtt_ssl"]
myCompName = read_mqtt_config()["client_name"]

mqtt_clientid = mqtt_clientid_prefix + myCompName #todo: comp name?
print("client id > " + mqtt_clientid)
client = mqtt.Client(mqtt_clientid)
client.tls_set()

#Assigning the object attribute to the Callback Function
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.on_publish = on_publish

print("connect >")
client.connect(mqtt_host, mqtt_port)
time.sleep(2)

mqtt_log_topic = mqtt_root_topic + "/" + myCompName + "/log"
print("Publishing message to topic: ",mqtt_log_topic)
client.publish(mqtt_log_topic,1) # topic, message (value) to publish
time.sleep(1)

print("> main loop ")
client.loop_start() #start the loop

loo = 0
while True:
	#getMess()
	#client.publish(mqtt_scroll_topic,mess) 
	time.sleep(20)
	loo = loo+1
	print("loop > " + str(loo))
