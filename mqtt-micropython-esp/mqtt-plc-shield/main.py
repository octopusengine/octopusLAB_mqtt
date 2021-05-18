# basic example: octopusLAB - ESP32 - PLC - MQTT
from time import sleep
from machine import Timer
from gc import mem_free

from utils.wifi_connect import read_wifi_config, WiFiConnect 
from utils.mqtt import MQTT
from utils.pinout import set_pinout
from utils.octopus_lib import i2c_init
from utils.bits import neg, reverse, int2bin, get_bit, set_bit

from components.plc.inputs.dummy import PLC_input_dummy
from components.plc.inputs.fixed import plc_input_fixed_high, plc_input_fixed_low
# from components.plc.elements.rs import PLC_element_RS
from components.plc.elements.rs_pulse import PLC_element_RS_pulse
from components.plc.operands.op_and import PLC_operand_AND
from components.plc.operands.op_or import PLC_operand_OR
from components.lm75 import LM75B
from components.led import Led
from components.i2c_expander import Expander8

print("mqtt-led.py > mqtt basic example")

print("--- RAM free ---> " + str(mem_free())) 

pinout = set_pinout()
led = Led(pinout.BUILT_IN_LED)

IN1, IN2, IN3, IN4     = 0, 1, 2, 3
OUT1, OUT2, OUT3, OUT4 = 4, 5, 6, 7
# OUT4 - signalization

timer_counter = 0
periodic = False
# tim1 = Timer(0)

print("--- PLC shield ---")
print("-"*50)

byte8 = 255 # all leds off


def plc_set(output,value):
     global byte8
     print(output,"->", value)
     byte8 = set_bit(byte8,output,value)
     exp8.write_8bit(byte8)
     sleep(0.1)


print("- I2C:")
i2c = i2c_init(True,200)
print(i2c.scan())
# 34 expander / 73 therm. / 84 eeprom

lm = LM75B(i2c)
temp = lm.get_temp()
print("- Temp: ", temp)

exp8 = Expander8(34)
print("- PCF:", exp8.read())

# bits4 = "0101"
# exp8.write_8bit(bits4)

for i in range(3):
    exp8.write_8bit(0)
    sleep(0.1)
    exp8.write_8bit(255)
    sleep(0.1)
    
exp8.write_8bit(set_bit(255,OUT1,0))
sleep(0.2)
exp8.write_8bit(set_bit(255,OUT2,0))
sleep(0.2)
exp8.write_8bit(set_bit(255,OUT3,0))
sleep(0.2)
exp8.write_8bit(set_bit(255,OUT4,0))

sleep(0.3)
exp8.write_8bit(255)


def simple_blink():
    led.value(1)
    sleep(0.5)
    led.value(0)
    sleep(0.5)


def mqtt_handler(topic, msg):
    global byte8
    print("MQTT handler {0}: {1}".format(topic, msg))
    data = bytes.decode(msg)

    if "led" in topic:
        print("led:", end='')        

        if data[0] == '1':  # oN
            print("-> on")
            led.value(1)
        elif data[0] == '0':  # ofF 
            print("-> off")
            led.value(0)
            sleep(0.1)

    if "do/1" in topic: # do = digital output
        if data == '1':  # on 
            #print("D1 -> 1")
            #byte8 = set_bit(byte8,OUT1,0)
            #exp8.write_8bit(byte8)
            plc_set(OUT1,0)
        elif data == '0':  # off 
            plc_set(OUT1,1)

    if "do/2" in topic:   
        if data == '1': plc_set(OUT2,0)
        elif data == '0': plc_set(OUT2,1)

    if "do/3" in topic:
        if data == '1': plc_set(OUT3,0)
        elif data == '0': plc_set(OUT3,1)


print("--- wifi_connect >")
net = WiFiConnect()
net.connect()

print("--- mqtt_connnect >")
# c = mqtt_connect_from_config(esp_id)
m = MQTT.from_config()
c = m.client

c.set_callback(mqtt_handler)
c.connect()
c.subscribe("octopus/device/{0}/#".format(m.client_id))
 
print("testing blink")
simple_blink()

print("send alive message")
c.publish("octopus/device", m.client_id) # topic, message (value) to publish

print("--- RAM free ---> " + str(mem_free()))
print("--- main loop >")
while True:
    c.check_msg()
    # sleep(5)
