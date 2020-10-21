WASA SCADA
----------------------------------

This repository contains all the Python modules for communicating with modbus devices which are used to retrieve data and send it to the server using mqtt protocol

## Contributors

- [Zahan Zib Sarwar Dhrubo](https://github.com/aurxine)
- [Foysal Khandakar Joy](https://github.com/fkhjoy)

## Documentation of the Modules
- [Energy Meter](#energy-meter)

## Energy Meter
This module contains 2 classes: 

```EnergyMeter_DZS100()```
We can create object with initialization and use methods of those classes like below. We just have to pass boolean value for those methods if we want to print or not.
```
dzs100 = EnergyMeter_DZS100(port='COM12', baudrate=9600, slaveAddress= 2)
combined_active_energy = dzs100.readCombinedActiveEnergy(print = False)
import_active_energy = dzs100.readImportActiveEnergy(print = False)
frequency = dzs100.readFrequency(print = False)
```
```EnergyMeter_DZS500()```
We can create object like DZS100. But we have to pass parameters to the methods based on the query. In ```readCurrent(self, phase = None, Print = True)``` method we have to pass the phase name as string among 'A', 'B', 'C'
```
current_A = dzs500.readCurrent(phase = 'A')
current_B = dzs500.readCurrent(phase = 'B'\)
```
In ```readVoltage(self, phase=None, line=None, Print = True)``` method we can read voltage of phase or voltage of line. We have to pass parameters based on the requirement. We can read voltage of phases 'A', 'B', 'C' or voltage of lines 'AB', 'BC', 'CA'
```
voltage_A = dzs500.readVoltage(phase = 'A')
voltage_AB = dzs500.readVoltage(line = 'AB')
```
In ```readPower(self, category, phase=None, Print = True)``` method we have several options for category and phase. For category we have 'active', 'reactive', 'apparent' and 'factor'. Foy phases 'A', 'B' and 'C'.
So if we want to read "Phase A active power" we can call the method like below
```
phaseA_activePower = dzs500.readPower(category = 'active', phase = 'A')
phaseB_reactivePower = dzs500.readPower(category = 'reactive', phase = 'B')
```



