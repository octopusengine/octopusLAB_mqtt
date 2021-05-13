#https://mntolia.com/mqtt-python-with-paho-mqtt-client/
import time
import paho.mqtt.client as mqtt
import requests, json, math

#broker_address = "yourmqtt/IP"
#broker_portno = 8883
#mqtt_root_topic ="octopus"

# kufr 2019/05
id_scroll = "30aea447aaa8" # esp device ID
id_keypad = "cc50e3b5d7ec" # =
id_socket = ""

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

mqtt_clientid = mqtt_clientid_prefix + "eee"
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

mqtt_log_topic = mqtt_root_topic + "/eee/log"
print("Publishing message to topic: ",mqtt_log_topic)
client.publish(mqtt_log_topic,123) # topic, message (value) to publish
time.sleep(1)

print("message from url test >")
#urlMess = "https://octopusengine.org/api/mess.json"
urlMess = "http://octopusengine.org/api/mess.json"
mess = "octopus test"
oldmess = mess

def getMess():
	global mess, oldmess
	try:
		response = requests.get(urlMess)
		url_json = json.loads(response.text)
		print(str(url_json))
		mess = url_json.get('message')
		print(mess)
	except:
		print("Err.loadCloudConfig() - connect? json exist?")     


topicAll ="octopus/#"
print("Subscribing to topic: ",topicAll)
client.subscribe(topicAll)

mqtt_scroll_topic = mqtt_root_topic + "/" + id_scroll + "/8x8mtx/scroll"
print("> scroll test: ",mqtt_scroll_topic)
client.publish(mqtt_scroll_topic,"eee-python") # topic, message (value) to publish
time.sleep(5)

mqtt_keypad_topic = mqtt_root_topic + "/" + id_keypad + "/wsled/rainbow"
print("> rainbow test: ",mqtt_keypad_topic)
client.publish(mqtt_keypad_topic,"") # topic, message (value) to publish
time.sleep(3)

print("> message scroll test: ",mqtt_scroll_topic)
getMess()
client.publish(mqtt_scroll_topic,mess) 
time.sleep(1)

#print("client.loop_forever() >")
#client.loop_forever()

print("> main loop ")
client.loop_start() #start the loop

loo = 0
while True:
	getMess()
	client.publish(mqtt_scroll_topic,mess) 
	time.sleep(20)
	loo = loo+1
	print("loop > " + str(loo))
