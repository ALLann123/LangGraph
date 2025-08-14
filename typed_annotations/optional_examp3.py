#!/usr/bin/python3
from typing import Optional

def nice_message(name:Optional[str])->None:
    if name is None:
        print("Hey random person!")

    else:
        print(f"Hi there, {name}!")

#get user input
name=input("Who gave the speech? ")

nice_message(None)

"""
N/B: Name can either be a string or None! 
Cannot be of any other type.
"""