from pymodbus.client.sync import ModbusSerialClient

def decode(lst):
    s = '0x'
    for x in lst:
        x = hex(x)
        s += x[2:]
    return int(s,0)


class EnergyMeter_DZS100():
    
    def __init__(self, method='rtu', port='/dev/ttyUSB0', baudrate=9600, timeout=3, parity='E', stopbits=1, bytesize=8, slaveAddress = 0):
        self.method = method
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.slaveAddress = slaveAddress
        self.client = ModbusSerialClient(
            method = self.method,
            port = self.port, #'/dev/ttyUSB0', #'COM9',
            baudrate = self.baudrate,
            timeout = self.timeout,
            parity = self.parity,
            stopbits = self.stopbits,
            bytesize = self.bytesize
        )
    def get_Address(self, address):
        self.slaveAddress = address
    
    def readCombinedActiveEnergy(self, Print = True):
        if self.client.connect():
            print("Connected to the Modbus Server/Slave")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=0, count=2, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
        else:
            print('Cannot connect to the Modbus Server/Slave')
    
    def readImportActiveEnergy(self, Print = True):
        if self.client.connect():
            print("Connected to the Modbus Server/Slave")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=2, count=2, unit = self.slaveAddress)
            
            if not res.isError():
                print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
        else:
            print('Cannot connect to the Modbus Server/Slave')
    
    def readExportActiveEnergy(self, Print = True):
        
        if self.client.connect():
            print("Connected to the Modbus Server/Slave")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=4, count=2, unit = self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
        else:
            print('Cannot connect to the Modbus Server/Slave')
    
    def readVoltage(self, Print = True):
        
        if self.client.connect():
            print("Connected to the Modbus Server/Slave")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=6, count=1, unit = self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
        else:
            print('Cannot connect to the Modbus Server/Slave')
    
    def readCurrent(self, Print = True):
        
        if self.client.connect():
            print("Connected to the Modbus Server/Slave")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=7, count=2, unit = self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
        else:
            print('Cannot connect to the Modbus Server/Slave')
    
    def readActivePower(self, Print = True):
        
        if self.client.connect():
            print("Connected to the Modbus Server/Slave")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=9, count=2, unit = self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
        else:
            print('Cannot connect to the Modbus Server/Slave')
    
    def readPowerFactor(self, Print = True):
        
        if self.client.connect():
            print("Connected to the Modbus Server/Slave")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=11, count=1, unit = self.slaveAddress)
            
            if not res.isError():
                print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
        else:
            print('Cannot connect to the Modbus Server/Slave')
    
    def readFrequency(self, Print = True):
        
        if self.client.connect():
            print("Connected to the Modbus Server/Slave")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=12, count=1, unit = self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
        else:
            print('Cannot connect to the Modbus Server/Slave')
            
    
# dsz100 = EnergyMeter_DZS100(port='COM10', baudrate=2400)

class EnergyMeter_DZS500():
    
    def __init__(self, method='rtu', port='/dev/ttyUSB0', baudrate=9600, timeout=3, parity='E', stopbits=1, bytesize=8, slaveAddress = 2):
        self.method = method
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.slaveAddress = slaveAddress
        self.client = ModbusSerialClient(
            method = self.method,
            port = self.port, #'/dev/ttyUSB0', #'COM9',
            baudrate = self.baudrate,
            timeout = self.timeout,
            parity = self.parity,
            stopbits = self.stopbits,
            bytesize = self.bytesize
        )
    def get_Address(self, address):
        self.slaveAddress = address
        
    def readCurrent(self, phase = None, Print = True):
        
        addr = None        
        if phase == None:
            print("Please call with phase")
            return
        
        if phase == 'A':
           addr = 16
        elif phase == 'B':
            addr = 17
        elif phase == 'C':
            addr = 18
        else:
            print("Please enter correct phase")
            return 
                
        if self.client.connect():
            print("Connected to the Modbus Server/Slave")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=addr, count=1, unit = self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
        else:
            print('Cannot connect to the Modbus Server/Slave')
    
    def readVoltage(self, phase=None, line=None, Print = True):
        
        addr = None        
        if phase == 'A':
            addr = 20
        elif phase == 'B':
            addr = 21
        elif phase == 'C':
            addr = 22
        elif line == 'AB':
            addr = 23
        elif line == 'BC':
            addr = 24
        elif line == 'CA':
            addr = 25
        else:
            print("Please enter valid input")
            return
                
        if self.client.connect():
            print("Connected to the Modbus Server/Slave")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=addr, count=1, unit = self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
        else:
            print('Cannot connect to the Modbus Server/Slave')
            
    def readPower(self, category, phase=None, Print = True):
        
        addr = None
        if phase == None:
            if category == 'active':
                addr = 26
            elif category == 'reactive':
                addr = 27
            elif category == 'apparent':
                addr = 28
            elif category == 'factor':
                addr = 29
                
        elif phase == 'A':
            if category == 'active':
                addr = 31
            elif category == 'reactive':
                addr = 34
            elif category == 'apparent':
                addr = 37
            elif category == 'factor':
                addr = 40
                
        elif phase == 'B':
            if category == 'active':
                addr = 32
            elif category == 'reactive':
                addr = 35
            elif category == 'apparent':
                addr = 38
            elif category == 'factor':
                addr = 41
                
        elif phase == 'C':
            if category == 'active':
                addr = 33
            elif category == 'reactive':
                addr = 36
            elif category == 'apparent':
                addr = 39
            elif category == 'factor':
                addr = 42
        if addr == None:
            print("Invalid input")
            return
   
        if self.client.connect():
            print("Connected to the Modbus Server/Slave")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=addr, count=1, unit = self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
        else:
            print('Cannot connect to the Modbus Server/Slave')

    def readBaudrate(self, Print = True):
        if self.client.connect():
            response = self.client.read_holding_registers(address= 129, count = 1, unit = self.slaveAddress)
            if not response.isError():
                if Print:
                    print(decode(response.registers))
                return decode(response.registers)
            else:
                print(response)
        else:
            print('Cannot connect to the Modbus Server/Slave')
    
    def changeBaudrate(self, baudrate = 9600, Print = True):
        if self.client.connect():
            response = self.client.write_register(address= 129, value = baudrate, unit = self.slaveAddress)
            if not response.isError():
                if Print:
                    print(response)
            else:
                print(response)
        else:
            print('Cannot connect to the Modbus Server/Slave')


    def writeTime(self, value, unit='seconds'):
        addr = None
        if unit=='seconds':
            addr = 500
        elif unit=='minutes':
            addr = 501
        elif unit=='hour':
            addr = 502
        elif unit=='week':
            addr = 503
        elif unit=='day':
            addr = 504
        elif unit=='month':
            addr = 505
        elif unit=='year':
            addr = 506
        else:
            print("Incorrect input")

        if self.client.connect():
            print("Connected to the Modbus Server/Slave")
            # Reading from a holding register with the below content.
            response = self.client.write_register(address=addr, value = value)
            print(response)
            
        else:
            print('Cannot connect to the Modbus Server/Slave')
    
    def changeAddress(self, address = 2, Print = True):
        if self.client.connect():
            response = self.client.write_register(address= self.slaveAddress, value = address,
            unit = self.slaveAddress)
            if Print:
                print(response)
        else:
            print('Cannot connect to the Modbus Server/Slave')
            
    
        
# dzs500 = EnergyMeter_DZS500( port='COM12', baudrate=9600, slaveAddress= 2)

#dzs500.readVoltage(phase= "A", Print= True)

#dzs500.changeBaudrate(baudrate= 9600)
#dzs100 = EnergyMeter_DZS100(port= 'COM12', baudrate= 2400, slaveAddress= 5)

# frequency = dzs100.readFrequency(Print= True)
# current = dzs100.readCurrent(Print= True)
# voltage = dzs100.readVoltage(Print= True)
# power = dzs100.readActivePower(Print= True)
# pf = dzs100.readPowerFactor(Print= True)

# print("Voltage:", voltage/10, "V")
# print("Current:", current/1000, "A")
# print("Power:", power/10000, "kW")
# print("Power Factor", pf/1000)
# print("Frequency:", frequency/100, "Hz")
        
            
            
        
