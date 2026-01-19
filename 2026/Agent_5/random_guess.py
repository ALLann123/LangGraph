#!/usr/bin/python3
import random

def guess_the_number():
    #Generate a random number between 1 and 20
    secret_number=random.randint(1, 20)

    print(f"Generate a random number between 1 and 20. Try to guess it!")

    #initialize  binary search bounds
    low=1
    high=20
    attempts=0

    while True:
        #make a guess using bianry search
        guess=(low+high)//2
        attempts+=1

        print(f"\nAttempt {attempts}: I guess {guess}")

        #check if guess is correct
        if guess==secret_number:
            print(f"Correct! The number was {secret_number}")
            print(f"It took me {attempts} attempts to guess it!")
            break

        #Get hint
        if guess< secret_number:
            print(f"Hint:Higher than {guess}")
            low=guess+1

        else:
            print(f"Hint: Lower than {guess}")
            high=guess-1

        #show current search range
        print(f"Search range updated: {low} to {high}")

guess_the_number()

"""
    cmd>> python random_guess.py
Generate a random number between 1 and 20. Try to guess it!

Attempt 1: I guess 10
Hint: Lower than 10
Search range updated: 1 to 9

Attempt 2: I guess 5
Hint: Lower than 5
Search range updated: 1 to 4

Attempt 3: I guess 2
Hint:Higher than 2
Search range updated: 3 to 4

Attempt 4: I guess 3
Hint:Higher than 3
Search range updated: 4 to 4

Attempt 5: I guess 4
Correct! The number was 4
It took me 5 attempts to guess it!
"""