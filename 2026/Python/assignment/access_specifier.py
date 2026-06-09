#!/usr/bin/python3

class BankAccount:
    # Class constructor. called on object creation
    def __init__(self, balance):
        self.__balance = balance #private attribute

    # method inside the class
    def get_balance(self):
        return self.__balance
    
# create an object
account=BankAccount(5000)

# Correct way is to invoke the method
print("Balance: ", account.get_balance())

# Wrongway and will throw an error trying to access private attributes
print(account.__balance)
