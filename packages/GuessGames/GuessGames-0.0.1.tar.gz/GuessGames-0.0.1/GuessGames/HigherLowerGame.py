from random import randint

def Play():
    first_int = randint(0,100) 
    print("Can you beat me? Consider integers from 0 to 100. I have the random integer {}.".format(first_int))
    answer = input("Will the next number be higher or lower?\n")
    while (answer!="higher")&(answer!="lower"):
        answer = input("Try again, please input either higher or lower? If you want to quit press Q.\n")
        if answer =="Q":
            break
    if answer!="Q":
        second_int = randint(0,100) 
        if ((first_int > second_int)&(answer=="lower"))|((first_int < second_int)&(answer=="higher")):
            print("Winner, your answer is correct. The next number was {}.".format(second_int))
        else:
            print("Loser, try again next time. The next number was {}.".format(second_int))
    else: 
        print("Goodbye")


if __name__=="__main__":
    Play()
    