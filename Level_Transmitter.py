import pymodbus
from pymodbus.client.sync import ModbusSerialClient
import numpy as np

def decode(lst):
    s = '0x'
    for x in lst:
        x = hex(x)
        s += x[2:]
    return int(s,0)

class AR6451():
    def __init__(self, method='rtu', port='COM9', baudrate=9600, timeout=3, parity='N', stopbits=1, 
    bytesize=8, slaveAddress = 1, m = 107.143, b = -91.36):
        self.method = method
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.slaveAddress = slaveAddress
        self.m = m
        self.b = b
        self.client = ModbusSerialClient(
            method = self.method,
            port = self.port,
            baudrate = self.baudrate,
            timeout = self.timeout,
            parity = self.parity,
            stopbits = self.stopbits,
            bytesize = self.bytesize
        )
    def get_Address(self, address):
        self.slaveAddress = address

    def readRegister(self, address = 0, Print = True):
        if self.client.connect():
            response = self.client.read_holding_registers(address = address, unit = self.slaveAddress)
            if not response.isError():
                if Print:
                    print(decode(response.registers))
                return decode(response.registers)
            else:
                print(response)
        else:
            print("Cannot connect to slave")
    
    def fitLine(self, Points):
        x = Points[0]
        y = Points[1]
        self.m, self.b = np.polyfit(x, y, 1)

    def Pressure(self, Print = True):
        pressure = self.readRegister(address = 4, Print = Print)
        dot_point = self.readRegister(address= 3, Print = Print)
        return pressure/(10**dot_point)
    
    def Water_Level(self, unit = 'cm', Print = True):
        if unit == 'cm':
            pressure = self.Pressure(Print = Print)
            return self.m*pressure + self.b
        if unit == 'm':
            pressure = self.Pressure(Print = Print)
            return (self.m*pressure + self.b)/100
        if unit == 'in':
            pressure = self.Pressure(Print = Print)
            return (self.m*pressure + self.b)*2.54

# level_sensor = AR6451()

