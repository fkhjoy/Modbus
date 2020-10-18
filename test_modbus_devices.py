from pymodbus.client.sync import ModbusSerialClient
import pymodbus

def decode(lst):
    s = '0x'
    for x in lst:
        x = hex(x)
        s += x[2:]
    return int(s,0)

class Modbus_Device():
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

    def readRegister(self, function_Code = 3, register = 0, count = 1, Print = True):
        if self.client.connect():
            if function_Code == 1:
                response = self.client.read_coils(address = register, count = count, unit = self.slaveAddress)
                
                if not response.isError():
                    print(decode(response.registers))
                    return decode(response.registers)
                else:
                    print(response)
            if function_Code == 2:
                response = self.client.read_discrete_inputs(address = register, count = count, unit = self.slaveAddress)
                
                if not response.isError():
                    print(decode(response.registers))
                    return decode(response.registers)
                else:
                    print(response)
            if function_Code == 3:
                response = self.client.read_holding_registers(address = register, count = count, unit = self.slaveAddress)
                
                if not response.isError():
                    print(decode(response.registers))
                    return decode(response.registers)
                else:
                    print(response)
            if function_Code == 4:
                response = self.client.read_input_registers(address = register, count = count, unit = self.slaveAddress)
                
                if not response.isError():
                    print(decode(response.registers))
                    return decode(response.registers)
                else:
                    print(response)



        else:
            print('Cannot connect to the Modbus Server/Slave')
