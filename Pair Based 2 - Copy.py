#function to recieve pico PWM
Value = 0
Detect = input("A Signal has been received from the first Pico! Y/N to measure.")
if Detect.lower == ("y"):
    print (Value)
