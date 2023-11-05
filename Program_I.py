'''This is the first program of two for the Pair-Based project. It contains 
the code that will set the PWM cycle, communicate that value to the second pico
via a serial interface, recieve the average calculated by the second pico and compare
it to the initial value of the PWM signal and display the value of the difference

Author: Nathan Savard
For the SED 1115 class
october 31 2023'''

from machine import PWM, Pin, UART
import time

#This function gets the value of the duty cycle from the user and makes it usable in a PWM object
def get_input():
    #()->float
    #set needed variables
    #flag used for the while loop
    noproperinput = True
    #maximum value of duty cycle that can be taken by a PWM object
    max_dutycycle = 65535   #2^16 - 1 because it is 16 bits
    #initialization of the duty_cycle variable that will be returned
    duty_cycle = 0

    #get the input from the user and ensure it can be used in the PWM object
    while noproperinput:
        #get input
        duty_cycle = float(input("Please enter the value of the PWM duty cycle in %: "))
        noproperinput = False
        #if input is wrong
        if (duty_cycle < 0 or duty_cycle > 100) or type(duty_cycle) != float:
            #set flag to restart loop 
            noproperinput = True
            print("Incorrect input. Please make sure the value is between 0 and 100.")
        else:
            #calculate the value so that duty_cycle can be used in the PWM object
            duty_cycle = int(max_dutycycle * (duty_cycle/100))
    #return the value of the duty_cycle that will be used for the PWM object
    return duty_cycle 

#this function sends the duty cycle given by the user to the other pico using uart communications
def send_PWM(duty_cycle):
    #(int)->None

    #set pin used for the PWM
    pwm_pin = Pin("GPIO2")  #pin chosen (pin number 3 will have the same freqency if used) 
    '''use the same in program II for simplicity'''
    
    #set the pwm object with the pin
    pwm = PWM(pwm_pin)
    #set the pwm base frequency (a lower frequency will help to have more counts of high and lows and thus more accuracy)
    pwm.freq(1000)
    #set the pwm duty cycle
    pwm.duty_u16(duty_cycle)

    #give a big enough time sample for the other program to accurately calculate the duty cycle
    time.sleep(2)

    #stop transmitting the signal
    pwm.deinit()

    # give some time so that the other code is ready to receive the duty cycle value (user input)
    time.sleep_ms(5)

#This function will send the inital value of the duty cycle to the other pico so that it can also compare the values
def send_duty_cycle(duty_cycle):
    #(int)->None

    #set UART
    uart = UART(0, 9600, tx=Pin("GPIO9"))

    #turn the duty cycle into a sendable binary variable
    duty_cycle_b = duty_cycle.encode('utf-8')

    #send the duty cycle value
    uart.write(duty_cycle_b)

#this function will receive the measured ananlog signal and return the value of the duty cycle (% and 0-65535)
def get_measured_signal():
    #()->int

    #set needed ariables
    data_bytes = False
    measured_duty_cycle = 0

    #set the pin that will receive the signal
    uart = UART(0, 9600, rx=Pin("GPIO9"))
    #set the flag for the while loop
    nothing_received = True
    #wait for the data and assign it to data_bytes
    while nothing_received:
        data_bytes = uart.read()
        if data_bytes != None or data_bytes != False:
            nothing_received = False
    #make sure the data_bytes is in bytes
    data_bytes = bytes(data_bytes)
    #turn the bytes values in a numeric value that can be used
    measured_duty_cycle = int(data_bytes.decode('utf-8'))
    
    #return the measured value of the PWM signal
    return measured_duty_cycle

#This function measures the difference between the duty cycle used and the one measured by the other pico
def measure_difference(measured_duty_cycle, duty_cycle):
    #(int, int)->int

    #get the value of the difference
    difference = abs(measured_duty_cycle-duty_cycle)

    #return the value of the difference
    return difference

#this function displays all the results to the user
def display_difference(difference, duty_cycle, measured_duty_cycle):
    #(int, int, int)->None

    #calculate duty cycles in % (p stands for percentage)
    measured_duty_cycle_p = (measured_duty_cycle / 65535) * 100
    duty_cycle_p = (duty_cycle / 65535) * 100
    difference_p = (difference / 65535) * 100

    #messages to the user
    print("The measure of the initial duty cycle; " + str(duty_cycle_p) + "% or " + str(measured_duty_cycle) + "/65535")
    print("The measure of the measured duty cycle; " + str(measured_duty_cycle_p) + "% or " + str(measured_duty_cycle) + "/65535")
    print("The difference between both is: " + str(difference_p) + "% or " + str(difference) + "/65535" )

duty_cycle = get_input()
send_PWM(duty_cycle)
send_duty_cycle(duty_cycle)
measured_duty_cycle = get_measured_signal()
difference = measure_difference(measured_duty_cycle, duty_cycle)
display_difference(difference, duty_cycle, measured_duty_cycle) 