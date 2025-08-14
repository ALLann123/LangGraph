#!/usr/bin/python3

"""
Lambda Functions are shortcuts to writing small functions.

"""
#Write a lambda function to calculate area?

#get measurements
num_one=int(input("Length: "))
num_two=int(input("width: "))

#area
area=lambda x,y:x*y

print(f"Area: {area(num_one,num_two)}")