import csv
from address import Address


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
                    distances = row[2:]
                    address_list.append(Address(id, formatted_address, distances))
                    id += 1
            Distances.__set_null_distances(address_list)
            return address_list
        except FileNotFoundError:
            raise FileNotFoundError("There is no CSV file for the distances.") from None
        except ValueError:
            raise ValueError("The distances are not in a valid format.") from None

    @classmethod
    def __set_null_distances(cls, address_list:list[Address]):
        for i in range(len(address_list)):
                for j in range(len(address_list[i].distances)):
                    if not address_list[i].distances[j]:
                        address_list[i].distances[j] = Distances.__set_null_distance(address_list, i, j)

    @classmethod
    def __set_null_distance(cls, address_list: list[Address],start_id: int, destination_id: id):
        try:
            if destination_id > start_id:
                return address_list[destination_id].distances[start_id]
            else:
                return address_list[start_id].distances[destination_id]
        except IndexError:
            raise IndexError("Out of range start or destination.") from None