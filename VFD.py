from pymodbus.client.sync import ModbusSerialClient

def decode(lst):
    s = '0x'
    for x in lst:
        x = hex(x)
        s += x[2:]
    return int(s,0)


class VFD_F800():
    
    def __init__(self, method='rtu', port='/dev/ttyUSB0', baudrate=9600, timeout=3,
     parity='E', stopbits=1, bytesize=8, slaveAddress = 0):
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
    
    def readOutputFrequency(self, Print=False):
        if self.client.connect():
            print("Connected to the Modbus Server/Slave")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=201, count=1, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
        else:
            print('Cannot connect to the Modbus Server/Slave')
            
    def readOutputCurrent(self, Print=False):
        if self.client.connect():
            print("Connected to the Modbus Server/Slave")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=202, count=1, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
        else:
            print('Cannot connect to the Modbus Server/Slave')
            
    def readOutputVoltage(self, Print=False):
        if self.client.connect():
            print("Connected to the Modbus Server/Slave")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=203, count=1, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
        else:
            print('Cannot connect to the Modbus Server/Slave')
    
    def readInputPower(self, Print=False):
        if self.client.connect():
            print("Connected to the Modbus Server/Slave")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=213, count=1, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
        else:
            print('Cannot connect to the Modbus Server/Slave')
            
    def readOutputPower(self, Print=False):
        if self.client.connect():
            print("Connected to the Modbus Server/Slave")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=214, count=1, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
        else:
            print('Cannot connect to the Modbus Server/Slave')
    
    def readCumulativePower(self, Print=False):
        if self.client.connect():
            print("Connected to the Modbus Server/Slave")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=225, count=1, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
        else:
            print('Cannot connect to the Modbus Server/Slave')
            
    def readOutputMotor(self, Print=False):
        if self.client.connect():
            print("Connected to the Modbus Server/Slave")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=234, count=1, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
        else:
            print('Cannot connect to the Modbus Server/Slave')
            
    def readRunningFrequency(self, Print=False):
        if self.client.connect():
            print("Connected to the Modbus Server/Slave")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=15, count=1, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
        else:
            print('Cannot connect to the Modbus Server/Slave')
