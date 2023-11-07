import time 
import random
#This function uses the random import to create a random number from the list provided.
def random_number():
    list = [1,2,3,4,5,6,7,8,9,10]
    num = random.random
    choice = random.choice(list)
    return choice

     
go = True
#The follwing while loop asks the user which number they pick, tells them if it was right and which number it actually was
# and also asks if they want to play again.
while go == True:
    Choose = input ("Hello, please guess a number!")
    #Choice is the choice that the computer chooses from the random function
    choice = random_number()
    #This detenrmines whether or not the number the user choose was the right number 
    if Choose == choice:
        again = input ("Wow you got it correct! Play again?")
        if again == 'Yes':
            print ("Restarting")
            time.sleep (1)
    else:
        print ("Sorry that was wrong. It was" + str(choice))
        time.sleep (2)
        again2 = input ("Play again?")
        if again2 == 'Yes':
            print ("Restarting")
            time.sleep (1)
        else: break
        
        
