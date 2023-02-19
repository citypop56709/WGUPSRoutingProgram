# A class that creates an address object.
# The address object associates address IDs with addresses and a list of distances.
# This makes it possible to work with all the necessary address information in one place
class Address:
    # Constructor for an address object.
    # Takes in an ID, based on the row ID in the CSV, an address, and a list of distances based on the info on the CSV.
    # The list of distances represents how many miles is the current address from every other possible address for delivery.
    def __init__(self, address_id: int, street_address:str, distances: list[float]):
        self.id = address_id
        self.street_address = street_address
        self.distances = distances