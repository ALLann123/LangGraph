#!/usr/bin/python3

# Question: Explain that SavingsAccount has access to deposits
# without redefining it again

# This is the parent/base class
class BankAccount:
    # Class constructor--> created when an object is created
    def __init__(self):
        self.deposits= []

    # Class method--> objects can invoke this
    def add_deposit(self, amount):
        self.deposits.append(amount)

# This is the derived or child class. Inheirts all attributes and methods from base class
# SavingsAccount inherits from BankAccount
class SavingsAccount(BankAccount):
    pass

# Object creation. Inherits all attributes and methods of the base class BankAccount
account = SavingsAccount()


# savingsAccount can access deposits directly
account.add_deposit(500)
account.add_deposit(1000)

print("Deposits:", account.deposits)

