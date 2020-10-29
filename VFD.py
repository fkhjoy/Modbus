from pymodbus.client.sync import ModbusSerialClient

def decode(lst):
    s = '0x'
    for x in lst:
        x = hex(x)
        s += x[2:]
    return int(s,0)

def toggle_bit(number, bit_position):
    return number^(1 << bit_position-1)

class VFD_F800():
    
    def __init__(self, client, slaveAddress = 0):
        
        self.slaveAddress = slaveAddress
        self.client = client
    
    def get_Address(self, address):
        self.slaveAddress = address
    
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
                return -1
        else:
            print('Cannot connect to the Modbus Server/Slave')
            return -1
            
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
                return -1
        else:
            print('Cannot connect to the Modbus Server/Slave')
            return -1
            
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
                return -1

        else:
            print('Cannot connect to the Modbus Server/Slave')
            return -1
    
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
                return -1
        else:
            print('Cannot connect to the Modbus Server/Slave')
            return -1
            
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
                return -1
        else:
            print('Cannot connect to the Modbus Server/Slave')
            return -1
    
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
                return -1
        else:
            print('Cannot connect to the Modbus Server/Slave')
            return -1
            
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
                return -1
        else:
            print('Cannot connect to the Modbus Server/Slave')
            return -1
            
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
                return -1
        else:
            print('Cannot connect to the Modbus Server/Slave')
            return -1

    def readRunningSpeed(self, Print=False):
        if self.client.connect():
            print("Connected to the Modbus Server/Slave")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=206, count=1, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
                return -1
        else:
            print('Cannot connect to the Modbus Server/Slave')
            return -1
            
    def readFaultHistory(self, Print = False):
        if self.client.connect():
            print("Connected to the Modbus Server/Slave")
            response = self.client.read_holding_registers(address = 501, count = 1, unit = self.slaveAddress)
            if not response.isError():
                Fault_code = decode(response.registers)
                return Fault_code
            else:
                print(response)
                return -1
        else:
            print('Cannot connect to the Modbus Server/Slave')
            return -1
            
    def writeRunningFrequency(self, frequency_value):
        if self.client.connect():
            print("Connected to the Modbus Server/Slave")
            # Writing to a holding register with the below content.
            self.client.write_register(address=15, value = frequency_value)
            
        else:
            print('Cannot connect to the Modbus Server/Slave')
            return -1


#vfd = VFD_F800(port= 'COM13', baudrate= 9600, slaveAddress= 6)

#vfd.readOutputPower(Print= True)