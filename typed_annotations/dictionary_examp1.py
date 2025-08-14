#!/usr/bin/python3
from typing import TypedDict

class Movie(TypedDict):
    name:str
    year:int


movie=Movie(name="Avengers Endgame", year=2019)

print("The movie: ", movie['name'])
print(f"Released: {movie['year']}")

"""
*****Advantages of the above******
Typed Safety
Enhanced Redability
"""

