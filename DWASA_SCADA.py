'''
This code will run in Rasspberry Pi. The code will do the following,
    1. Retrieve data from VFD, Level Transmitter, Energy meter and AMR.
    2. Format the acquired data as json and send it to the broker with a unique topic
    3. Subscribe to that unique topic and receive commands
    4. Take actions according to those commands
'''
#! /usr/bin/env python

# pylint: disable=unused-variable
# pylint: enable=too-many-lines

import paho.mqtt.client as mqtt
import time
from datetime import datetime
import json
from random import seed
from random import randint
from Energy_Meter import EnergyMeter_DZS500
from Level_Transmitter import AR6451
from VFD import VFD_F800
import os
from AMR import AMR
from pymodbus.client.sync import ModbusSerialClient
import sys


class SCADA_Devices():
    def __init__(self, port = '/dev/ttyUSB0', method='rtu', baudrate=9600, timeout=3, 
        parity='E', stopbits=1, bytesize=8, vfd_slaveAddress = 6, energy_meter_slaveAddress = 3, 
        level_transmitter_slaveAddress = 2, amr_mode = 'BCM', amr_pin = 24, amr_flow_per_pulse = 10,
        amr_past_water_flow = None, ID = None, data_sending_period = 60):
        
        #Read ID from file
        
        if ID != None:
            self.ID_file = open("ID.txt", 'x')
            self.ID_file.write(str(ID))
        else:
            current_folder = os.path.dirname(os.path.abspath(__file__))
            ID_file = os.path.join(current_folder, 'ID.txt')
            self.ID_file = open(ID_file, 'r')
            ID = int(self.ID_file.read())
        self.ID = ID
        self.ID_file.close()
        
        self.port = port
        self.method = method
        self.baudrate = baudrate
        self.timeout = timeout
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.client = ModbusSerialClient(
            method = self.method,
            port = self.port,
            baudrate = self.baudrate,
            timeout = self.timeout,
            parity = self.parity,
            stopbits = self.stopbits,
            bytesize = self.bytesize
        )

        self.VFD = VFD_F800(client = self.client, slaveAddress= vfd_slaveAddress)
        self.Level_Transmitter = AR6451(client = self.client, slaveAddress= level_transmitter_slaveAddress)
        self.Energy_Meter = EnergyMeter_DZS500(client = self.client, slaveAddress= energy_meter_slaveAddress)
        self.AMR = AMR(mode= amr_mode, pin= amr_pin, flow_per_pulse= amr_flow_per_pulse, past_water_flow = amr_past_water_flow)
        
        self.data_sending_period = data_sending_period
        self.mqtt_client = mqtt.Client("Client", transport= 'websockets')
        self.mqtt_client.on_message = self.on_message
        self.command = ''
        self.last_command = ''
        self.mqtt_pub_topic = 'scada_test'
        self.mqtt_sub_topic = 'scada_sub'
        
        self.SCADA_Data = {
                "ID":1500,
                "Time_Stamp":"2019-11-06 16:04:52",
                "Data_Sending_Period": 60,
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
    
    def get_MQTT_Address(self, address = '123.49.33.109'):
        self.mqtt_address = address

    def get_MQTT_Port(self, port):
        self.mqtt_port = port

    def get_MQTT_Connection_Data(self, address, port):
        self.mqtt_address = address
        self.mqtt_port = port

    def MQTT_Address(self):
        return self.mqtt_address
    
    def MQTT_Port(self):
        return self.mqtt_port
    
    def on_message(self, client, userdata, message):
        Message = str(message.payload.decode("utf-8"))
        self.command = Message
        print("message received:", Message)
    
    def is_New_Command(self):
        if self.last_command != self.command:
            self.last_command = self.command
            return True
        return False
    
    def get_Sub_Topic(self, topic):
        self.mqtt_sub_topic = topic
    
    def get_Pub_Topic(self, topic):
        self.mqtt_pub_topic = topic

    def connect(self):
        self.mqtt_client.connect(self.MQTT_Address(), self.MQTT_Port())

    
    def disconnect(self):
        self.mqtt_client.disconnect()
    
    def subscribe(self, topic = None):
        if topic == None:
            self.mqtt_client.subscribe(self.mqtt_sub_topic)
        else:
            self.mqtt_sub_topic = topic
            self.mqtt_client.subscribe(self.mqtt_sub_topic)
    
    def publish(self, topic = None, payload = ''):
        if topic == None:
            self.mqtt_client.publish(self.mqtt_pub_topic, payload)
        else:
            self.mqtt_pub_topic = topic
            self.mqtt_client.publish(self.mqtt_pub_topic, payload)
    
    def loop(self):
        self.mqtt_client.loop()

    def get_ID(self, ID):
        self.ID = ID
        self.ID_file = open('ID.txt', 'w+')
        self.ID_file.write(str(ID))
        self.ID_file.close()

    def get_VFD_Address(self, address = 0):
        self.VFD.get_Address(address= address)
    
    def get_Energy_Meter_Address(self, address = 3):
        self.Energy_Meter.get_Address(address= address)
    
    def get_Level_Transmitter_Address(self, address = 2):
        self.Level_Transmitter.get_Address(address= address)

    def get_AMR_Flow_Per_Pulse(self, flow_per_pulse):
        self.AMR.get_flow_per_pulse(flow_per_pulse= flow_per_pulse)
    
    def get_AMR_Flow_Unit(self, flow_unit):
        self.AMR.get_flow_unit(flow_unit= flow_unit)
    
    def get_AMR_Time_Unit(self, time_unit):
        self.AMR.get_time_unit(time_unit= time_unit)

    def reset_Counter(self):
        self.AMR.reset_counter()
        
    def makeTimeStamp(self):
        now = datetime.now()
        self.formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        return self.formatted_date_time
    
    def parameterQuery(self, type = '', parameter = ''): # returns parameters
        self.updateParameters()

        if len(type) > 0:
            return self.SCADA_Data[type][parameter]
        else:
            return self.SCADA_Data[parameter]
    
    def is_json(self, myjson):
        try:
            json_object = json.loads(myjson)
        except ValueError as e:
            return False
        return True

    def executeCommand(self, json_command):
        if self.is_json(json_command):
            command = json.loads(json_command)
        else:
            self.mqtt_client.publish(self.mqtt_pub_topic, "Wrong json format")
            return 0

        if command["Command"] == "Query":
            self.mqtt_client.publish(self.mqtt_pub_topic, self.parameterQuery(type = command["Type"], parameter = command["Parameter"]))
        elif command["Command"] == "Change_ID":
            self.get_ID(command["ID"])
            self.publish(self.mqtt_pub_topic, "New ID set successfully!")
        elif command["Command"] == "Change_Data_Sending_Period":
            self.data_sending_period = command["Data_Sending_Period"]
            self.publish(self.mqtt_pub_topic, "New period set successfully!")
        elif command["Command"] == "Change_MQTT_Data":
            self.get_MQTT_Connection_Data(command["Address"], command["Port"])
            self.publish(self.mqtt_pub_topic, "New MQTT data set successfully!")
            #self.disconnect() # disconnect from previous IP
            self.connect() # connect to new IP
            #self.subscribe(self.mqtt_sub_topic)
        elif command["Command"] == "Change_Topic":
            self.mqtt_client.unsubscribe(self.mqtt_sub_topic)
            self.mqtt_pub_topic = command["Pub_Topic"]
            self.mqtt_sub_topic = command["Sub_Topic"]
            self.mqtt_client.subscribe(self.mqtt_sub_topic)
        
        # elif command["Command"] == "ON":
        #     self.VFD.VFD_ON()
        #     self.publish(self.mqtt_pub_topic, "VFD Turned ON")
        
        # elif command["Command"] == "ON":
        #     self.VFD.VFD_OFF()
        #     self.publish(self.mqtt_pub_topic, "VFD Turned OFF")

        else:
            self.publish(self.mqtt_pub_topic, "Error in command")
            


    def updateParameters(self, Print = False, random = False):
        self.SCADA_Data["ID"] = self.ID
        self.SCADA_Data["Time_Stamp"] = self.makeTimeStamp()
        self.SCADA_Data["Data_Sending_Period"] = self.data_sending_period

        if not random:
            self.SCADA_Data["Energy"]["Phase_A_Voltage"] = self.Energy_Meter.readVoltage(phase= 'A', Print = Print)
            self.SCADA_Data["Energy"]["Phase_B_Voltage"] = self.Energy_Meter.readVoltage(phase= 'B', Print = Print)
            self.SCADA_Data["Energy"]["Phase_C_Voltage"] = self.Energy_Meter.readVoltage(phase= 'C', Print = Print)
            self.SCADA_Data["Energy"]["Line_AB_Voltage"] = self.Energy_Meter.readVoltage(line= 'AB', Print = Print)
            self.SCADA_Data["Energy"]["Line_BC_Voltage"] = self.Energy_Meter.readVoltage(line= 'BC', Print = Print)
            self.SCADA_Data["Energy"]["Line_CA_Voltage"] = self.Energy_Meter.readVoltage(line= 'CA', Print = Print)
            self.SCADA_Data["Energy"]["Phase_A_Current"] = self.VFD.readOutputPower(Print = Print)/self.Energy_Meter.readVoltage(phase= 'A', Print = Print)
            self.SCADA_Data["Energy"]["Phase_B_Current"] = self.VFD.readOutputPower(Print = Print)/self.Energy_Meter.readVoltage(phase= 'B', Print = Print)
            self.SCADA_Data["Energy"]["Phase_C_Current"] = self.VFD.readOutputPower(Print = Print)/self.Energy_Meter.readVoltage(phase= 'C', Print = Print)
            self.SCADA_Data["Energy"]["Active_Power"] = self.VFD.readOutputPower(Print = Print)
            self.SCADA_Data["Energy"]["Power_Factor"] = self.VFD.readOutputPower(Print = Print)/self.VFD.readInputPower(Print = Print)
            self.SCADA_Data["Energy"]["Load"] = (self.SCADA_Data["Energy"]["Active_Power"]**2 - self.SCADA_Data["Energy"]["Power_Factor"]**2)**0.5
            
            if self.SCADA_Data["Energy"]["Load"] != 0:
                self.SCADA_Data["VFD"]["VFD_Status"] = 1
            else:
                self.SCADA_Data["VFD"]["VFD_Status"] = 0
            self.SCADA_Data["VFD"]["Frequency"] = self.VFD.readOutputFrequency(Print= Print)
            self.SCADA_Data["VFD"]["Motor_Operating_Voltage"] = self.VFD.readOutputVoltage(Print= Print)
            self.SCADA_Data["VFD"]["Motor_Operating_Current"] = self.VFD.readOutputCurrent(Print= Print)
            self.SCADA_Data["VFD"]["RPM"] = 3000#self.VFD.readRunningSpeed(Print= Print)

            self.SCADA_Data["Water_Data"]["Water_Flow"] = 2 + randint(-5, 5) * 0.1#self.AMR.flow_rate()
            self.SCADA_Data["Water_Data"]["Water_Pressure"] = 341 # random value
            self.SCADA_Data["Water_Data"]["Water_Meter_Reading"] = self.SCADA_Data["Water_Data"]["Water_Meter_Reading"] + self.SCADA_Data["Water_Data"]["Water_Flow"] * self.data_sending_period
            self.SCADA_Data["Water_Data"]["Water_Level"] = 50#self.Level_Transmitter.Water_Level(Print= Print)
        else:
            self.SCADA_Data["Energy"]["Phase_A_Voltage"] = self.Energy_Meter.readVoltage(phase= 'A', Print = Print)
            self.SCADA_Data["Energy"]["Phase_B_Voltage"] = self.Energy_Meter.readVoltage(phase= 'B', Print = Print)
            self.SCADA_Data["Energy"]["Phase_C_Voltage"] = self.Energy_Meter.readVoltage(phase= 'C', Print = Print)
            self.SCADA_Data["Energy"]["Line_AB_Voltage"] = self.Energy_Meter.readVoltage(line= 'AB', Print = Print)
            self.SCADA_Data["Energy"]["Line_BC_Voltage"] = self.Energy_Meter.readVoltage(line= 'BC', Print = Print)
            self.SCADA_Data["Energy"]["Line_CA_Voltage"] = self.Energy_Meter.readVoltage(line= 'CA', Print = Print)
            self.SCADA_Data["Energy"]["Active_Power"] = self.VFD.readOutputPower()
            self.SCADA_Data["Energy"]["Phase_A_Current"] = self.SCADA_Data["Energy"]["Active_Power"]*1000/self.SCADA_Data["Energy"]["Phase_A_Voltage"]
            self.SCADA_Data["Energy"]["Phase_B_Current"] = self.SCADA_Data["Energy"]["Active_Power"]*1000/self.SCADA_Data["Energy"]["Phase_B_Voltage"]
            self.SCADA_Data["Energy"]["Phase_C_Current"] = self.SCADA_Data["Energy"]["Active_Power"]*1000/self.SCADA_Data["Energy"]["Phase_C_Voltage"]
            
            self.SCADA_Data["Energy"]["Power_Factor"] = 0.45 + randint(-2, 2)/10
            self.SCADA_Data["Energy"]["Load"] = (self.SCADA_Data["Energy"]["Active_Power"]**2 - self.SCADA_Data["Energy"]["Power_Factor"]**2)**0.5
            
            if self.SCADA_Data["Energy"]["Load"] != 0:
                self.SCADA_Data["VFD"]["VFD_Status"] = 1
            else:
                self.SCADA_Data["VFD"]["VFD_Status"] = 0
            self.SCADA_Data["VFD"]["Frequency"] = 50
            self.SCADA_Data["VFD"]["Motor_Operating_Voltage"] = self.SCADA_Data["Energy"]["Line_AB_Voltage"]
            self.SCADA_Data["VFD"]["Motor_Operating_Current"] = self.SCADA_Data["Energy"]["Phase_A_Current"]
            self.SCADA_Data["VFD"]["RPM"] = 2100

            self.SCADA_Data["Water_Data"]["Water_Flow"] = 1000
            self.SCADA_Data["Water_Data"]["Water_Pressure"] = 341 # random value
            self.SCADA_Data["Water_Data"]["Water_Meter_Reading"] += self.SCADA_Data["Water_Data"]["Water_Flow"]
            self.SCADA_Data["Water_Data"]["Water_Level"] = 25

        return json.dumps(self.SCADA_Data)


init = {}

with open(sys.argv[1]) as file:
    text = f.read()

    for line in text.split('\n'):
        d = line.split(',')
        init[d[0]] = d[1]


SCADA = SCADA_Devices(port=init['port'], method=init['method'], baudrate=init['baudrate'], timeout=init['timeout'],
    parity=init['parity'], stopbits=int(init['stopbits']), bytesize=int(init['bytesize']), vfd_slaveAddress=int(init['vfd_slaveAddress']),
    energy_meter_slaveAddress=int(init['energy_meter_slaveAddress']), level_transmitter_slaveAddress=int(init['level_transmitter_slaveAddress']),
    amr_mode=init['amr_mode'], amr_pin=int(init['amr_pin']), amr_flow_per_pulse=int(init['amr_flow_per_pulse']),
    amr_past_water_flow=init['amr_past_water_flow'], ID=init['ID'], data_sending_period=init['data_sending_period'])


broker = init['broker_address'] #'123.49.33.109' #MQTT broker address
port = init['broker_port'] #8083 #MQTT broker port
SCADA.get_MQTT_Address(broker)
SCADA.get_MQTT_Port(port)
SCADA.get_Sub_Topic('scada_sub') # Topic to publish
SCADA.get_Pub_Topic('scada_test') # Topic to subscribe

SCADA.connect()
SCADA.subscribe()

delay_time = SCADA.data_sending_period

tic = time.time()

while True:
    SCADA.loop()
    toc = time.time()

    if (toc - tic) >= delay_time:
        SCADA_Data_Json = SCADA.updateParameters(random= False, Print = True)
        print(SCADA_Data_Json)
        SCADA.publish(payload= SCADA_Data_Json)
        tic = toc
    
    if SCADA.is_New_Command():
        print(SCADA.command)
        SCADA.executeCommand(SCADA.command)

    else:
        continue
    
    
