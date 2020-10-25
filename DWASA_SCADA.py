'''
This code will run in Rasspberry Pi. The code will do the following,
    1. Retrieve data from VFD, Level Transmitter, Energy meter and AMR.
    2. Format the acquired data as json and send it to the broker with a unique topic
    3. Subscribe to that unique topic and receive commands
    4. Take actions according to those commands
'''
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


# class for all the devices in the SCADA

class SCADA_Devices():
    def __init__(self, port = '/dev/ttyUSB0', vfd_slaveAddress = 0,
    energy_meter_slaveAddress = 2, level_transmitter_slaveAddress = 1, 
    amr_mode = 'BCM', amr_pin = 23, amr_flow_per_pulse = 10, amr_past_water_flow = 100000):
        self.ID = 1500
        self.port = port
        self.VFD = VFD_F800(port= port, slaveAddress= vfd_slaveAddress)
        self.Level_Transmitter = AR6451(port= port, slaveAddress= level_transmitter_slaveAddress)
        self.Energy_Meter = EnergyMeter_DZS500(port= port, slaveAddress= energy_meter_slaveAddress)
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

    def makeTimeStamp(self):
        now = datetime.now()
        self.formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        return self.formatted_date_time
    
    def query(self, type, parameter):
        self.updateParameters()
        return self.SCADA_Data[type][parameter]

    def updateParameters(self, Print = False):
        self.SCADA_Data["ID"] = self.ID
        self.SCADA_Data["Time_Stamp"] = self.makeTimeStamp()

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
    SCADA_Data_Json = SCADA.updateParameters()
    client.publish(Pub_Topic, SCADA_Data_Json)

    if prev_Message != Message:
        print(Message)
        prev_Message = Message
        Command = json.loads(Message)
    else:
        continue
    
    
