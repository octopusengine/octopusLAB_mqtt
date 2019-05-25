"""
octopusLAB (c) 2019
simple setup mqtt to config file: config/mqtt.json

"""

#TODO DRY for filename
import time, os, requests, json, math
import paho.mqtt.client as mqtt

ver = "0.1 / 25.5.2019"
mqtt = ""

octopuASCII = [
"      ,'''`.",
"     /      \ ",
"     |(@)(@)|",
"     )      (",
"    /,'))((`.\ ",
"   (( ((  )) ))",
"   )  \ `)(' / ( ",
]

def mainOctopus():
    for ol in octopuASCII:
        print(str(ol))
    print()

def setupMenu():
    print()
    print('=' * 30)
    print('      M Q T T    S E T U P')
    print('=' * 30)
    print("[ms]  - mqtt setup")
    print("[mt]  - mqtt simple test")
    print("[si]  - system info")
    print("[e]   - exit mqtt setup")

    print('=' * 30)
    sel = input("select: ")
    return sel
    
def read_mqtt_config():
    # TODO file does not exist
    f = open('config/mqtt.json', 'r')
    d = f.read()
    f.close()
    return json.loads(d)    

def mqtt():
    global mqtt
    mainOctopus()
    print("Hello, this will help you initialize MQTT")
    print("ver: " + ver + " (c)octopusLAB")
    print("Press Ctrl+C to abort")
    
    # TODO improve this
    # prepare directory
    if 'config' not in os.listdir():
       os.makedirs('config')

    run= True
    while run:
        sele = setupMenu()

        if sele == "e":
            print("Setup - exit >")
            time.sleep(1)
            run = False

        if sele == "si": 
            #from util.sys_info import sys_info
            #sys_info()
            print("[mqtt]")
            try:
               with open('config/mqtt.json', 'r') as f:
                    d = f.read()
                    f.close()
               print(" > config/mqtt: " + d)
            except:
               print("'config/mqtt.json' does not exist")
    
        if sele == "ms":
            print("Set mqtt >")
            print()
            mq = {}
            mq['mqtt_broker_ip'] = input("BROKER IP: ")
            mq['mqtt_ssl'] = int(input("> SSL (0/1): "))
            mq['mqtt_port'] = int(input("> PORT (1883/8883/?): "))
            mq['mqtt_clientid_prefix'] = input("CLIENT PREFIX: ")
            mq['mqtt_root_topic'] = input("ROOT TOPIC: ")
            mq['client_name'] = input("your computer name: ")
            print("Writing to file config/mqtt.json")
            with open('config/mqtt.json', 'w') as f:
                json.dump(mq, f)

        def mqtt_sub(topic, msg):  
            print("MQTT Topic {0}: {1}".format(topic, msg))                

        if sele == "mt":
            print("mqtt simple test:")   
			
            print("mqtt_config >")
            mqtt_clientid_prefix = read_mqtt_config()["mqtt_clientid_prefix"]
            mqtt_host = read_mqtt_config()["mqtt_broker_ip"]
            mqtt_root_topic = read_mqtt_config()["mqtt_root_topic"]
            #mqtt_ssl  = False # Consider to use TLS!
            mqtt_ssl  = read_mqtt_config()["mqtt_ssl"]

            mqtt_clientid = mqtt_clientid_prefix + "eee"
            print("clientid > " + mqtt_clientid)
            client = mqtt.Client(mqtt_clientid)
            client.tls_set()
            
            print("mqtt.connect to " + mqtt_host)
            print("connect >")
            client.connect(broker_address, broker_portno)
            time.sleep(2)

            mqtt_log_topic = mqtt_root_topic + "/eeepc/log"
            print("Publishing message to topic: ",mqtt_log_topic)
            client.publish(mqtt_log_topic,123) # topic, message (value) to publish
            time.sleep(1)

            """
            # c.subscribe("/octopus/device/{0}/#".format(esp_id))
            subStr = mqtt_root_topic+"/"+esp_id+"/#"
            print("subscribe (root topic + esp id):" + subStr)
            c.subscribe(subStr)
            """

               
mqtt()
print("end / ok")