'''This is the first program of two for the Pair-Based project. It contains 
the code that will set the PWM cycle, communicate that value to the second pico
via a serial interface, recieve the average calculated by the second pico and compare
it to the initial value of the PWM signal and display the value of the difference

Author: Nathan Savard
For the SED 1115 class
october ___ 2023'''

from machine import PWM, Pin
import time

#This function gets the value of the duty cycle
def get_input():
    #()->float
    flag = True
    while flag:
        duty_cycle = float(input("Please enter the value of the PWM duty cycle in %: "))
        flag = False
        if duty_cycle < 0 or duty_cycle > 100 or type(duty_cycle) != float:     #Ensure the value is appropriate 
            flag = True
            print("Incorrect input. Please make sure the value is between 0 and 100.")
    return duty_cycle

def set_PWM_signal(duty_cycle):
    #(float)->pwm

    #Set the pin
    pin = #pin number

    