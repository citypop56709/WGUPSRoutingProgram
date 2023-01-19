import math
import pandas as pd
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
        try:
            distance_data = pd.read_excel(rf"{file_path}", skiprows=7)
            for i in range(distance_data.shape[0]):
                raw_address = distance_data.iloc[i][0]
                formatted_address = raw_address.split("(")[0].strip()
                distances = []
                for j in range(2, distance_data.shape[1]):
                    distances.append(distance_data.iloc[i][j])
                address_list.append(Address(i, formatted_address, distances))
            Distances.__set_null_distances(address_list)
            return address_list
        except FileNotFoundError:
            raise FileNotFoundError("There is no excel file for the distances.") from None
        except ValueError:
            raise ValueError("The distances are not in a valid format.") from None
    @classmethod
    def __set_null_distances(cls, address_list:list[Address]):
        for i in range(len(address_list)):
                for j in range(len(address_list[i].distances)):
                    if math.isnan(address_list[i].distances[j]):
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