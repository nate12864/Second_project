import time

import machine

def calculate_duty_cycle(input_pin):
    input_pin = 3
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

time.sleep(10)
##puts some time inbetween the functions as to keep them accurate

def receive_initial_duty_cycle(uart_port):
    # Initialize variables
    data_buffer = b''  # A byte buffer to store received data

    # Initialize the UART
    uart = machine.UART(uart_port, baudrate=9600)  # Replace baudrate with the appropriate value

    # Wait for the start of the signal (assuming start signal is high)
    while uart.read(1) != b'\xFF':
        pass

    # Start receiving data
    receiving_data = True

    while receiving_data:
        data = uart.read(1)

        if data == b'\xFF':
            receiving_data = False
        else:
            data_buffer += data

    # Convert received data to an integer (16-bit value)
    initial_duty_cycle = int.from_bytes(data_buffer, 'big')

    return initial_duty_cycle



def send_duty_cycle(uart_port, duty_cycle):
    # Initialize the UART
    uart = machine.UART(uart_port, baudrate=9600)  # Replace baudrate with the appropriate value

    # Send a start signal (e.g., '\xFF') to indicate the beginning of data
    uart.write(b'\xFF')

    # Send the duty cycle as a 16-bit value
    duty_cycle_bytes = duty_cycle.to_bytes(2, 'big')
    uart.write(duty_cycle_bytes)


