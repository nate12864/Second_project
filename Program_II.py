import time
import machine
from machine import UART
duty_cycle = 0
received_number = 0
def calculate_duty_cycle(input_pin):
    input_pin = 2
    # Initialize variables for highs and lows of the duty cycle
    highs = 0
    lows = 0
    # Configure the input pin
    pin = machine.Pin(input_pin, machine.Pin.IN)
    # Wait for a high signal to start receiving data
    while not pin.value():
        time.sleep_ms(1)
    # Start receiving data (placeholder for when second pico posts up)
    cap = 0
    
    received_data = uart.read(2)  # Read 2 bytes for the duty cycle
    if received_data is not None and uart.any():
        uart.read()
        receiving_data = True

        while receiving_data:
            #Stops recieving the data once there have been 1000 lows
            if cap >= 1000:
                lows -= 1000 ##makes sure that the second after the cycle stops there aren't any leftoever lows
                receiving_data = False
                continue
            if pin.value() == 0:  ##value is a function which will get the boolean value of a pin, either 1 or 0. In this 0 represents...
                ##...a low signal, and therefore the program adds 1 to the low count. Chat gpt was used to find this function and decide that it was...
                ##...the best fit for this scenario.
                lows += 1
                cap += 1
                time.sleep_ms(1)
            else:  ## If the pin value isn't zero that means it must be 1, and therefore the program adds one to the high counter. Additionally...
                ##... both the above if statement and this else statement have timesleep functions which,
                highs += 1
                cap = 0
                time.sleep_ms(1)
        if highs == 0:
            return 0  # The duty cycle was 0% because there were no highs
        # Calculate duty cycle out of 65535
        duty_cycle = int((highs / (highs + lows)) * 65535)
        return duty_cycle
        time.sleep(0.01)
    else: print ("Data is not being recieved")



uart_port = 2  
baudrate = 9600  #sets the transfer rate
# Initialize UART with the appropriate parameters
uart = machine.UART(uart_port, baudrate=baudrate)

#function to recieve the data of what the user inputed from the other pico...Chat gpt assisted in making this function
def receive_initial_duty_cycle(uart_port, baudrate=9600):
    try:
        uart = machine.UART(uart_port, baudrate=baudrate)
        received_data = uart.read(2)  # Read 2 bytes for the initial duty cycle

        if received_data is not None and len(received_data) == 2: #makes sure that data is being recieved, the len function makes sure that the recieved data is 2 bytes
            initial_duty_cycle = int.from_bytes(received_data) #converts from bytes to a readable (for the user) integer
            return initial_duty_cycle
        else: 
            print("Number was not received correctly.")
            return None
# additional error checking
    except Exception as e:
        print("Error:", e)
        return None

#This final function will send the measured cycle to the first pico
def send_duty_cycle(duty_cycle):
     
    uart = UART(2, 9600,) #sets bauderate and pin number

  #converts into a binary variable
    duty_cycle_b = duty_cycle.encode('utf-8')

 #actually sends the variable
    uart.write(duty_cycle_b)
#This while loop is the primary part of the code the user will be interacting with, and utilises the functions.
go = True
while go == True:
    step1 = input("Hello, would you like to recieve and calculate the duty cycle from PICO 1? Y/N")
    if step1.lower() == 'y':
        num = input ("Which pin are you using?")
        calculate_duty_cycle(num)
        time.sleep (1)
        print ("Here is the duty cycle calculated:" + str(duty_cycle))
        step2 = input("Next, would you like to read and measure the difference between the current duty cycel and the intial duty cycle inputed into the first program? Y/N")
        if step2.lower() == 'y':
            uart_port = num
            initial_duty_cycle = receive_initial_duty_cycle(uart_port)

            if initial_duty_cycle is not None:
                print("Received initial duty cycle:", initial_duty_cycle)
            else:
                print("Failed to receive initial duty cycle.")
                break
            #Total is the difference between original and measured duty cycles.
            Total = duty_cycle - initial_duty_cycle
            print ("Calculated difference between intital, and measured:" + str(Total) )
            time.sleep(1)
            print ("The data will now be sent back to the original pico.")
            send_duty_cycle(duty_cycle)
            asker  = input ("Would you like to exit the program? Y/N")
            if asker.lower() == 'y':
                break
            else:
                continue







