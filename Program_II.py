import time

import machine
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
    receiving_data = True
    cap = 0
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
#puts some time inbetween the functions as to keep them accurate



# Initialize UART with the appropriate parameters
uart_port = 2  # Replace with the actual UART port number you are using
baudrate = 9600  #sets the transfer rate

uart = machine.UART(uart_port, baudrate=baudrate)

received_data = uart.read(2)  # Read 2 bytes since we are assuming a 16-bit number

if received_data is not None and len(received_data) == 2: ##as we are reading 2 bytes each, this makes sure that data is recieved, and that it is 2 bytes
    received_number = int.from_bytes(received_data, 'big')  # Convert received bytes back to an integer
    print("Received inital duty cycle that the user inputed:", received_number)
else:
    print("Number was not recieved corretly")

int1 = duty_cycle  # Replace with your first integer
int2 = received_number  # Replace with your second integer

int1_bytes = int1.to_bytes(2, 'big')  # Assuming 2-byte integers in big-endian format
int2_bytes = int2.to_bytes(2, 'big')

uart.write(int1_bytes)
uart.write(int2_bytes)






