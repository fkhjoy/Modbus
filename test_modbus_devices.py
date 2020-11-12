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
            port = self.port, #'/dev/ttyUSB0'or #'COM9',
            baudrate = self.baudrate,
            timeout = self.timeout,
            parity = self.parity,
            stopbits = self.stopbits,
            bytesize = self.bytesize
        )

    def readRegister(self, function_Code = 3, register = 0, count = 1, Print = True):
        if self.client.connect():
            print('Client connected')
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
                print('Reading holding regisster')
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
    
    def writeRegister(self, function_Code = 6, register = 0, count = 1, Print = True, value = 0):
        if self.client.connect():
            if function_Code == 6:
                if count > 1:
                    response = self.client.write_registers(address= register, values= value, unit = self.slaveAddress)
                    if not response.isError():
                        print("Written Successfully!")
                    else:
                        print("Error Writing")
                else:
                    response = self.client.write_register(address= register, value= value, unit = self.slaveAddress)
                    if not response.isError():
                        print("Written Successfully!")
                    else:
                        print("Error Writing")
            if function_Code == 5:
                response = self.client.write_coil(address= register, values= value, unit = self.slaveAddress)
                if not response.isError():
                    print("Written Successfully!")
                else:
                    print("Error Writing")

# dzs500 = Modbus_Device(port = 'COM11', slaveAddress = 2)

# dzs500.readRegister(register= 30)

# level_sensor = Modbus_Device(port= 'COM9', slaveAddress= 1, parity= 'N')
# #level_sensor.writeRegister(register= 2, value= 3)

# P = level_sensor.readRegister(register= 4)

# water_level = 107.143*(P/1000 - 1.058) + 22
# print("Water level", "{:.2f}".format(water_level), "cm")

vfd = Modbus_Device(port= 'COM9', slaveAddress= 6, parity= 'E')
vfd.readRegister(register= 8, Print= True)