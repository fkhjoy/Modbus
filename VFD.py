from pymodbus.client.sync import ModbusSerialClient
import RPi.GPIO as GPIO
import time

def decode(lst):
    s = '0x'
    for x in lst:
        x = hex(x)
        s += x[2:]
    return int(s,0)

def toggle_bit(number, bit_position):
    return number^(1 << bit_position-1)

class VFD_F800():
    
    def __init__(self, client, On_pin = 25, Off_pin = 26, slaveAddress = 0):
        
        self.slaveAddress = slaveAddress
        self.client = client
        self.On_pin = On_pin
        self.Off_pin = Off_pin
        GPIO.setup(GPIO.BCM)
        GPIO.setup(self.On_pin, GPIO.OUT)
        GPIO.setup(self.Off_pin, GPIO.OUT)
    
    def VFD_ON(self):
        GPIO.output(self.On_pin, 1)
        time.sleep(1)
        GPIO.output(self.On_pin, 0)
    
    def VFD_OFF(self):
        GPIO.output(self.Off_pin, 1)
        time.sleep(1)
        GPIO.output(self.Off_pin, 0)

    def get_Address(self, address):
        self.slaveAddress = address
    
    def readOutputFrequency(self, Print=False):
        if self.client.connect():
            print("Connected to the VFD")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=200, count=1, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
                return -1
        else:
            print('Cannot connect to the VFD')
            return -1
            
    def readOutputCurrent(self, Print=False):
        if self.client.connect():
            print("Connected to the VFD")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=201, count=1, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
                return -1
        else:
            print('Cannot connect to the VFD')
            return -1
            
    def readOutputVoltage(self, Print=False):
        if self.client.connect():
            print("Connected to the VFD")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=202, count=1, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
                return -1

        else:
            print('Cannot connect to the VFD')
            return -1
    
    def readInputPower(self, Print=False):
        if self.client.connect():
            print("Connected to the VFD")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=212, count=1, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
                return -1
        else:
            print('Cannot connect to the VFD')
            return -1
            
    def readOutputPower(self, Print=False):
        if self.client.connect():
            print("Connected to the VFD")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=213, count=1, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
                return -1
        else:
            print('Cannot connect to the VFD')
            return -1
    
    def readCumulativePower(self, Print=False):
        if self.client.connect():
            print("Connected to the VFD")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=224, count=1, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
                return -1
        else:
            print('Cannot connect to the VFD')
            return -1
            
    def readOutputMotor(self, Print=False):
        if self.client.connect():
            print("Connected to the VFD")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=233, count=1, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
                return -1
        else:
            print('Cannot connect to the VFD')
            return -1
            
    def readRunningFrequency(self, Print=False):
        if self.client.connect():
            print("Connected to the VFD")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=14, count=1, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
                return -1
        else:
            print('Cannot connect to the VFD')
            return -1

    def readRunningSpeed(self, Print=False):
        if self.client.connect():
            print("Connected to the VFD")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=205, count=1, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
                return -1
        else:
            print('Cannot connect to the VFD')
            return -1
            
    def readFaultHistory(self, Print = False):
        if self.client.connect():
            print("Connected to the VFD")
            response = self.client.read_holding_registers(address = 500, count = 1, unit = self.slaveAddress)
            if not response.isError():
                Fault_code = decode(response.registers)
                return Fault_code
            else:
                print(response)
                return -1
        else:
            print('Cannot connect to the VFD')
            return -1
            
    def writeRunningFrequency(self, frequency_value):
        if self.client.connect():
            print("Connected to the VFD")
            # Writing to a holding register with the below content.
            self.client.write_register(address=14, value = frequency_value)
            
        else:
            print('Cannot connect to the VFD')
            return -1


#vfd = VFD_F800(port= 'COM13', baudrate= 9600, slaveAddress= 6)

#vfd.readOutputPower(Print= True)