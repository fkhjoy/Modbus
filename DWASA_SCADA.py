'''
This code will run in Rasspberry Pi. The code will do the following,
    1. Retrieve data from VFD, Level Transmitter and Energy meter
    2. Format the acquired data as json and send it to the broker with a unique topic
    3. Subscribe to that unique topic and receive commands
    4. Take actions according to those commands

To-do for Foysal:
    1. Complete VFD write method. Two registers are to be written in,
        (i) Holding register 15, which is for Frequency. Writable range is 1-590Hz.
        (ii) Holding register 9, which is for Control Input command. Read page 475 of VFD manual
        for details.
    2. Add Level Transmitter, Energy meter and VFD classes to the main code. Make them easily accessable
    and configurable.
'''

