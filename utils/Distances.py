import csv
from address import Address
from hash_table import HashTable


class Distances:
    """
    Creates a graph that stores in distances a tuple for each address. Each address has an ID based on where it is in excel.
    When retrieving the distance we can find out the distance to and from by checking if the destination is before or after the start
    as far as ID. This enables us to retrieve a distance to a location and back from a location relatively easily.
    """
    @classmethod
    def get_addresses_from_file(cls, file_path: str):
        address_list = []
        id = 0
        try:
            file = open(file_path)
            distance_data = csv.reader(file)
            for i, row in enumerate(distance_data):
                if i > 7:
                    raw_address = row[1]
                    formatted_address = raw_address.split("(")[0].strip()
                    #The distances come as strings so we have to convert them.
                    distances = [float(x) for x in row[2:] if x]
                    address_list.append(Address(id, formatted_address, distances))
                    id += 1
            #After the distances are created we then replace the missing values with the correct ones.
            Distances.set_null_distances(address_list)
            return address_list
        except FileNotFoundError:
            raise FileNotFoundError("There is no CSV file for the distances.") from None
        except ValueError:
            raise ValueError("The distances are not in a valid format.") from None

    @classmethod
    def get_address_table(cls, address_list: list[Address]) -> HashTable:
        address_table = HashTable()
        for address in address_list:
            address_table.put(address.street_address, address)
        return address_table

    @classmethod
    def set_null_distances(cls, address_list:list[Address]) -> None:
        for i in range(len(address_list)):
            for j in range(len(address_list)):
                try:
                    address_list[i].distances[j]
                except IndexError:
                    address_list[i].distances.append(address_list[j].distances[i])