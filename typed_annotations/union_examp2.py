#!/usr/bin/python3
from typing import Union

def square(x: Union[int, float]) -> float:
    return x*x

x=5
print(square(5))
x=9.22
print(square(x))

"""
*** Advantages of Unions***
1) Flexible and easy to code
2)Type Safety. Able to catch run time errors
"""