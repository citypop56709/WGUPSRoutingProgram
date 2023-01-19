"""
A class that creates an address object. The point of this class is to make it easier to associate addresses with
distances and an ID.
"""


class Address:
    def __init__(self, address_id: int, address:str, distances: list[int]):
        self.id = address_id
        self.address = address
        self.distances = distances
