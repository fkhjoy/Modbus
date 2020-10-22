'''
This code will run in Rasspberry Pi. The code will do the following,
    1. Retrieve data from VFD, Level Transmitter, Energy meter and AMR.
    2. Format the acquired data as json and send it to the broker with a unique topic
    3. Subscribe to that unique topic and receive commands
    4. Take actions according to those commands

To-do for Foysal:
    1. Complete VFD write method. Two registers are to be written in,
        (i) Holding register 15, which is for Frequency. Writable range is 1-590Hz.
        (ii) Holding register 9, which is for Control Input command. Read page 475 of VFD manual
        for details.
    2. Add Level Transmitter, Energy meter and VFD classes to the main code. Make them easily accessable
    and configurable.
To-do for Dhrubo:
    1. Make a class for AMR
    2. Make a class for SCADA data comprising of all the device classes. The object will have 
    a dictionary, this will help us for querry
'''
import paho.mqtt.client as mqtt
import time
from datetime import datetime
import json
from random import seed
from random import randint

seed(1)

# Json format for mqtt data sending

SCADA_Data = {
   "ID":1500,
   "Time_Stamp":"2019-11-06 16:04:52",
   "Energy":{
      "Phase_A_Voltage":223.4,
      "Phase_B_Voltage":223.4,
      "Phase_C_Voltage":223.4,
      "Line_AB_Voltage":403.2,
      "Line_BC_Voltage":443.13,
      "Line_CA_Voltage":392.2,
      "Phase_A_Current":77.4,
      "Phase_B_Current":76.5,
      "Phase_C_Current":75.45,
      "Active_Power":213,
      "Power_Factor":0.56,
      "Load":54.2
   },
   "VFD":{
      "VFD_Status":1,
      "Frequency":50.1,
      "Motor_Operating_Voltage":234.1,
      "Motor_Operating_Current":77,
      "RPM":2414
   },
   "Water_Data":{
      "Water_Flow":10000,
      "Water_Pressure":341,
      "Water_Meter_Reading":1234131,
      "Water_Level":32
   }
}

def makeTimeStamp():
    now = datetime.now()
    formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_date_time

def updateParameters():
    global SCADA_Data
    SCADA_Data["Time_Stamp"] = makeTimeStamp()
    SCADA_Data["Energy"]["Phase_A_Voltage"] = 230 + randint(-10, 10)
    SCADA_Data["Energy"]["Phase_B_Voltage"] = 230 + randint(-10, 10)
    SCADA_Data["Energy"]["Phase_C_Voltage"] = 230 + randint(-10, 10)
    SCADA_Data["Energy"]["Phase_A_Current"] = 70 + randint(-10, 10)
    SCADA_Data["Energy"]["Phase_B_Current"] = 70 + randint(-10, 10)
    SCADA_Data["Energy"]["Phase_C_Current"] = 70 + randint(-10, 10)
    SCADA_Data["Energy"]["Line_AB_Voltage"] = 230 + randint(-10, 10)
    SCADA_Data["Energy"]["Line_BC_Voltage"] = 230 + randint(-10, 10)
    SCADA_Data["Energy"]["Line_CA_Voltage"] = 230 + randint(-10, 10)
    SCADA_Data["Energy"]["Active_Power"] = 200 + randint(-10, 10)
    SCADA_Data["Energy"]["Power_Factor"] = 0.5 + randint(-10, 10)/100
    SCADA_Data["Energy"]["Load"] = 54 + randint(-10, 10)

    SCADA_Data["VFD"]["Frequency"] = 50 + randint(-10, 10)/100
    SCADA_Data["VFD"]["Motor_Operating_Voltage"] = 230 + randint(-10, 10)
    SCADA_Data["VFD"]["Motor_Operating_Current"] = 75 + randint(-5, 5)

    SCADA_Data["Water_Data"]["Water_Flow"] = 10000 + randint(-100, 100)
    SCADA_Data["Water_Data"]["Water_Pressure"] = 350 + randint(-10, 10)
    SCADA_Data["Water_Data"]["Water_Meter_Reading"] += SCADA_Data["Water_Data"]["Water_Flow"]
    SCADA_Data["Water_Data"]["Water_Level"] = 32 + randint(-10, 10)/100

    return json.dumps(SCADA_Data)



Message = "" #<String> this will store the json foramtted Messages from dashboard
prev_Message = "" #For checking repeated comands
def on_message(client, userdata, message):
    global Message
    Message = str(message.payload.decode("utf-8"))
    print("message received:", Message)
    # print("message topic=",message.topic)
    # print("message qos=",message.qos)
    # print("message retain flag=",message.retain)

broker = '123.49.33.109' #MQTT broker address
port = 8083 #MQTT broker port
Pub_Topic = 'scada_test' # Topic to publish
Sub_Topic = 'DMA/Sub/SCADA' # Topic to subscribe

client = mqtt.Client(transport= 'websockets')
client.connect(broker, port)
client.on_message = on_message

print("Subscribing to topic",Sub_Topic)
client.subscribe(Sub_Topic)


while True:
    time.sleep(10)
    client.loop()
    SCADA_Data_Json = updateParameters()
    client.publish(Pub_Topic, SCADA_Data_Json)

    if prev_Message != Message:
        print(Message)
        prev_Message = Message
        Command = json.loads(Message)
    else:
        continue
    
    
