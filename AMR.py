'''
This class is for reading water flow from AMR
'''
import RPi.GPIO as GPIO  
import time

class AMR():
    def __init__(self, mode = 'BCM', pin = 23, flow_unit = 'cm', time_unit = 'min',
                 flow_per_pulse = 1, past_water_flow = 0):
        self.flow_unit = flow_unit
        self.time_unit = time_unit
        # Water passed for each pulse in the sensor
        self.flow_per_pulse = flow_per_pulse
        # Water already passed
        self.past_water_flow = past_water_flow
        # Make a file for saving past water
        # w = create a file for writing, if it's not already there
        # + = both read nad write
        self.file = open('Water_Passed.txt', 'w+') 
        self.file.write(str(self.past_water_flow))
        self.file.close()
        # pin numbering mode.
        # 'BCM' means using GPIO numbering
        # 'BOARD' means using pin numbering with respect to the board
        # 'BCM' is preferred
        self.mode = mode
        # The pin to which sensors one terminal is connected
        # The other terminal is connected to Gnd
        self.pin = pin
        # This counts the number of pulse
        self.pulse_count = 0
        # This one is for measureing the flow per unit time
        self.prev_pulse_count = 0
        
        # This is for keeping track of water flow per unit time
        self.tic = time.time()
        self.toc = 0
        
        # This will be used for unit conversion
        # Standard unit for time is 1 second and standard unit for volume is 1 cubic meter (cm)
        # All parameters are converted to the standard unit
        self.units = {'min' : 60, 'second' : 1, 'hour' : 3600, 'day' : 24*3600, 'L' : 1000, 'cm' : 1}
        
        
        if self.mode == 'BCM':
            GPIO.setmode(GPIO.BCM)
        elif self.mode == 'BOARD':
            GPIO.setmode(GPIO.BOARD)
        else:
            print("Incorrect Mode!")
        
        # Pin is set to Input Pullup.
        # This way noise will be canceled
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Adding Interrupt callback function
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback = self.pulse_counter, bouncetime = 200)
        
    def pulse_counter(self, channel):
        self.pulse_count += 1
        print(self.pulse_count)
    
    def get_flow_unit(self, flow_unit = 'cm'):
        self.flow_unit = flow_unit
    
    def get_time_unit(self, time_unit = 'second'):
        self.time_unit = time_unit
    
    def get_flow_per_pulse(self, flow_per_pulse):
        self.flow_per_pulse = flow_per_pulse
    
    def get_past_water_flow(self, past_water_flow):
        self.past_water_flow = past_water_flow
        self.file = open('Water_Passed.txt', 'w+') 
        self.file.write(str(self.past_water_flow))
        self.file.close()
    
    def print_current_count(self):
        print(self.pulse_count)

    def total_water_passed(self):
        self.file = open('Water_Passed.txt', 'r') 
        self.past_water_flow = int(self.file.read())
        self.file.close()
        total_water = self.past_water_flow + self.pulse_count*self.flow_per_pulse
        return total_water*self.units[self.flow_unit]
    
    def total_water_passed_unit(self):
        return self.flow_unit
    
    def flow_rate(self):
        self.toc = time.time()
        elapsed_time = (self.toc - self.tic)/self.units[self.time_unit]
        #print("Time elapsed:", elapsed_time)
        self.tic = time.time()
        water_flow = ((self.pulse_count - self.prev_pulse_count)*self.flow_per_pulse)*self.units[self.flow_unit]
        #print("Water Flow:", water_flow)
        self.prev_pulse_count = self.pulse_count
        if elapsed_time != 0:
            return water_flow/elapsed_time
        else:
            return 0
    
    def flow_rate_unit(self):
        return self.flow_unit + "/" + self.time_unit
    
    def convertTo(self, flow_unit = 'cm', time_unit = 'second'):
        self.flow_unit = flow_unit
        self.time_unit = time_unit
    
    def reset_counter(self):
        self.pulse_count = 0
        self.prev_pulse_count = 0

amr = AMR()

while True:  
    time.sleep(5)
    f = amr.flow_rate()
    print(f, amr.flow_rate_unit())
    #amr.reset_counter()

