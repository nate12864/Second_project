import time
import machine

def calculate_duty_cycle():
    #()->int
    # Initialize variables for highs and lows of the duty cycle
    highs = 0
    lows = 0
    # Configure the input pin
    pin = machine.Pin(machine.Pin("GPIO2"), machine.Pin.IN)

    # Wait for a high signal to start receiving data
    while not pin.value():
        time.sleep(0.5)

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
            time.sleep_us(1)
        else:  ## If the pin value isn't zero that means it must be 1, and therefore the program adds one to the high counter. Additionally...
            ##... both the above if statement and this else statement have timesleep functions which,
            highs += 1
            cap = 0
            time.sleep_us(1)

    if highs == 0:
        return 0  # The duty cycle was 0% because there were no highs

    # Calculate duty cycle out of 65535
    duty_cycle = int((highs / (highs + lows)) * 65535)
    return duty_cycle

def receive_initial_duty_cycle():
    # Initialize variables
    #initialize the variable containing the binary form of the recieved duty cycle
    data_bytes = False

    # Initialize the UART
    uart = machine.UART(0, baudrate=9600, rx=machine.Pin("GPIO9"))  # Replace baudrate with the appropriate value

    # Start receiving data
    not_recieving_data = True

    #wait for the data and assigne it to data_bytes
    while not_recieving_data:
        data_bytes = uart.read()
        if data_bytes != None or data_bytes != False:
            not_recieving_data = False

    #make sure the data_bytes variable is of the bytes type
    data_bytes = bytes(data_bytes)
    # Convert received data to an integer (16-bit value)
    initial_duty_cycle = data_bytes.decode("utf-8")

    return initial_duty_cycle

def send_duty_cycle(duty_cycle):
    # Initialize the UART
    uart = machine.UART(0, baudrate=9600, tx=machine.Pin("GPIO9"))  # Replace baudrate with the appropriate value

    #transfer the calaculated duty cycle into a byte value that will be transmitted
    duty_cycle_bytes = duty_cycle.encode("utf-8")
    #send the duty cycle through the UART
    uart.write(duty_cycle_bytes)


pwm_duty_cycle = calculate_duty_cycle()
user_duty_cycle = receive_initial_duty_cycle()
send_duty_cycle(pwm_duty_cycle)

def tot():
    Total = pwm_duty_cycle - int(user_duty_cycle)
    return Total


pwm_duty_cycle = calculate_duty_cycle()
user_duty_cycle = receive_initial_duty_cycle()
send_duty_cycle(pwm_duty_cycle)

go = True
while go == True:
    step1 = input("Hello, would you like to recieve and calculate the duty cycle from PICO 1? Y/N")
    if step1.lower() == 'y':
        calculate_duty_cycle()
        time.sleep (1)
        print ("Here is the duty cycle calculated:" + str(pwm_duty_cycle))
        step2 = input("Next, would you like to read and measure the difference between the current duty cycel and the intial duty cycle inputed into the first program? Y/N")
        if step2.lower() == 'y':
            if user_duty_cycle is not None:
                print("Received initial duty cycle:", user_duty_cycle)
            else:
                print("Failed to receive initial duty cycle.")
                break
            #Total is the difference between original and measured duty cycles.
            Total = tot()
            print ("Calculated difference between intital, and measured:" + str(Total) )
            time.sleep(1)
            print ("The data will now be sent back to the original pico.")
            send_duty_cycle(pwm_duty_cycle)
            asker  = input ("Would you like to exit the program? Y/N")
            if asker.lower() == 'y':
                break
            else:
                continue