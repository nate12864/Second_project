import time

import machine

def calculate_duty_cycle(input_pin):
    # Initialize variables
    highs = 0
    lows = 0
    total_count = 0

    # Configure the input pin
    pin = machine.Pin(input_pin, machine.Pin.IN)

    # Wait for a high signal to start receiving data
    while not pin.value():
        time.sleep_ms(1)

    # Start receiving data
    receiving_data = True

    while receiving_data:
        if lows >= 1000:
            lows -= 1000
            receiving_data = False

        if pin.value() == 0:  # Low signal
            lows += 1
            time.sleep_ms(1)
        else:  # High signal
            highs += 1
            time.sleep_ms(1)

    if highs == 0:
        return 0  # The duty cycle was 0% because there were no highs

    # Calculate duty cycle out of 65535
    duty_cycle = int((highs / (highs + lows)) * 65535)
    return duty_cycle

time.sleep(10)


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


