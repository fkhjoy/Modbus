'''
This code will run in Rasspberry Pi. The code will do the following,
    1. Retrieve data from VFD, Level Transmitter, Energy meter and AMR.
    2. Format the acquired data as json and send it to the broker with a unique topic
    3. Subscribe to that unique topic and receive commands
    4. Take actions according to those commands
'''
#! /usr/bin/env python

import paho.mqtt.client as mqtt
import time
from datetime import datetime
import json
from random import seed
from random import randint
from Energy_Meter import EnergyMeter_DZS500
from Level_Transmitter import AR6451
from VFD import VFD_F800
from AMR import AMR
from pymodbus.client.sync import ModbusSerialClient
from subprocess import call

# calls an echo in the terminal
call(['DWASA_SCADA.py running'], shell=True)

# class for all the devices in the SCADA

class SCADA_Devices():
    def __init__(self, port = '/dev/ttyUSB0', method='rtu', baudrate=9600, timeout=3, 
        parity='E', stopbits=1, bytesize=8, vfd_slaveAddress = 0, energy_meter_slaveAddress = 3, 
        level_transmitter_slaveAddress = 2, amr_mode = 'BCM', amr_pin = 23, amr_flow_per_pulse = 10, amr_past_water_flow = 100000):
        self.ID = 1500
        self.port = port
        self.method = method
        self.baudrate = baudrate
        self.timeout = timeout
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.client = ModbusSerialClient(
            method = self.method,
            port = self.port, #'/dev/ttyUSB0', #'COM9',
            baudrate = self.baudrate,
            timeout = self.timeout,
            parity = self.parity,
            stopbits = self.stopbits,
            bytesize = self.bytesize
        )

        self.VFD = VFD_F800(client = self.client, slaveAddress= vfd_slaveAddress)
        self.Level_Transmitter = AR6451(client = self.client, slaveAddress= level_transmitter_slaveAddress)
        self.Energy_Meter = EnergyMeter_DZS500(client = self.client, slaveAddress= energy_meter_slaveAddress)
        self.AMR = AMR(mode= amr_mode, pin= amr_pin, flow_per_pulse= amr_flow_per_pulse, past_water_flow= amr_past_water_flow)
        self.SCADA_Data = {
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
    
    def get_ID(self, ID):
        self.ID = ID

    def get_VFD_Address(self, address = 0):
        self.VFD.get_Address(address= address)
    
    def get_Energy_Meter_Address(self, address = 2):
        self.Energy_Meter.get_Address(address= address)
    
    def get_Level_Transmitter_Address(self, address = 1):
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
    
    def query(self, type, parameter):
        self.updateParameters()
        return self.SCADA_Data[type][parameter]

    def updateParameters(self, Print = False, random = False):
        self.SCADA_Data["ID"] = self.ID
        self.SCADA_Data["Time_Stamp"] = self.makeTimeStamp()

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
            self.SCADA_Data["VFD"]["RPM"] = self.VFD.readRunningSpeed(Print= Print)

            self.SCADA_Data["Water_Data"]["Water_Flow"] = self.AMR.flow_rate()
            self.SCADA_Data["Water_Data"]["Water_Pressure"] = 341 # random value
            self.SCADA_Data["Water_Data"]["Water_Meter_Reading"] = self.AMR.total_water_passed()
            self.SCADA_Data["Water_Data"]["Water_Level"] = self.Level_Transmitter.Water_Level(Print= Print)
        else:
            self.SCADA_Data["Energy"]["Phase_A_Voltage"] = self.Energy_Meter.readVoltage(phase= 'A', Print = Print)
            self.SCADA_Data["Energy"]["Phase_B_Voltage"] = self.Energy_Meter.readVoltage(phase= 'B', Print = Print)
            self.SCADA_Data["Energy"]["Phase_C_Voltage"] = self.Energy_Meter.readVoltage(phase= 'C', Print = Print)
            self.SCADA_Data["Energy"]["Line_AB_Voltage"] = self.Energy_Meter.readVoltage(line= 'AB', Print = Print)
            self.SCADA_Data["Energy"]["Line_BC_Voltage"] = self.Energy_Meter.readVoltage(line= 'BC', Print = Print)
            self.SCADA_Data["Energy"]["Line_CA_Voltage"] = self.Energy_Meter.readVoltage(line= 'CA', Print = Print)
            self.SCADA_Data["Energy"]["Active_Power"] = 30 + randint(-50, 50)/10
            self.SCADA_Data["Energy"]["Phase_A_Current"] = self.SCADA_Data["Energy"]["Active_Power"]*1000/self.Energy_Meter.readVoltage(phase= 'A', Print = Print)
            self.SCADA_Data["Energy"]["Phase_B_Current"] = self.SCADA_Data["Energy"]["Active_Power"]*1000/self.Energy_Meter.readVoltage(phase= 'B', Print = Print)
            self.SCADA_Data["Energy"]["Phase_C_Current"] = self.SCADA_Data["Energy"]["Active_Power"]*1000/self.Energy_Meter.readVoltage(phase= 'C', Print = Print)
            
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


SCADA = SCADA_Devices()

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
    SCADA_Data_Json = SCADA.updateParameters(random= True)
    client.publish(Pub_Topic, SCADA_Data_Json)

    if prev_Message != Message:
        print(Message)
        prev_Message = Message
        Command = json.loads(Message)
    else:
        continue
    
    
