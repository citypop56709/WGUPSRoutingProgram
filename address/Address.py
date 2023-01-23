"""
A class that creates an address object. The point of this class is to make it easier to associate addresses with
distances and an ID.
"""


class Address:
    """
    When I made this class I had to separate address from street address to improve readability.
    """
    def __init__(self, address_id: int, street_address:str, distances: list[float]):
        self.id = address_id
        self.street_address = street_address
        self.distances = distances