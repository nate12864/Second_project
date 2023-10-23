'''This is the first program of two for the Pair-Based project. It contains 
the code that will set the PWM cycle, communicate that value to the second pico
via a serial interface, recieve the average calculated by the second pico and compare
it to the initial value of the PWM signal and display the value of the difference

Author: Nathan Savard
For the SED 1115 class
october ___ 2023'''

from machine import PWM, Pin, UART
import time
import sys

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

def setPWM(duty_cycle):
    #(int)->machine.PWM

    #set pin used for the PWM
    pwm_pin = Pin(2)  #pin chosen (pin number 3 will have the same freqency if used) 
    '''use the same in program II for simplicity'''

    #set the pwm object with the pin
    pwm = PWM(pwm_pin)
    #set the pwm base frequency (a higher frequency so raise the accuracy of the measure of the analog signal)
    pwm.freq(120000000)
    #set the pwm duty cycle
    pwm.duty_u16(duty_cycle)

    #return the pwm object to be activated later
    return pwm

#this function will receive the measured ananlog signal and return the value of the duty cycle (% and 0-65535)
def get_measured_signal():
    #()->int, int

    #set needed ariables
    measured_duty_cycle_bin = None
    measured_duty_cycle = 0

    #set the pin that will receive the signal
    uart = UART(0, 9600, rx=Pin(8)) ;'''tx in the other program should be Pin(8)'''
    #set the flag for the while loop
    nothing_received = True
    #receive the signal
    while nothing_received:
        #if data is being transmitted
        if uart.any():
            #get the data
            measured_duty_cycle_bin = uart.read()
            #check if there is data, if the previous if passed through then the value shouldn't be None
            if measured_duty_cycle_bin != None:
                measured_duty_cycle = int(measured_duty_cycle_bin.decode('utf=8'))    ;'''should be out of 65535'''
            else:
                #this never should happen but it would mean that the value received is None
                print("there seems to be an error in the signal because the value of the received signal is None")
                #exit the program to adjust input or connections of the hardware
                sys.exit()
            #end the loop
            nothing_received = False
    
    #return the measured value of the PWM signal
    return measured_duty_cycle

#This function measures the difference between the duty cycle used and the one measured by the other pico
def measure_difference(measured_duty_cycle, duty_cycle):
    #(float, float)->float

    #get the value of the difference
    difference = abs(measured_duty_cycle-duty_cycle)

    #return the value of the difference
    return difference

def display_difference(difference, duty_cycle, measured_duty_cycle):
    #(float, int, int)->None

    #calculate duty cycles in % (p stands for percentage)
    measured_duty_cycle_p = (measured_duty_cycle / 65535) * 100
    duty_cycle_p = (duty_cycle / 65535) * 100
    difference_p = (difference / 65535) * 100

    #messages to the user
    print("The measure of the initial duty cycle; " + str(duty_cycle_p) + "% or " + str(measured_duty_cycle) + "/65535")
    print("The measure of the measured duty cycle; " + str(measured_duty_cycle_p) + "% or " + str(measured_duty_cycle) + "/65535")
    print("The difference between both is: " + str(difference_p) + "% or " + str(difference) + "/65535" )