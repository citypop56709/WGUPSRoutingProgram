import math
import pandas as pd

from hash_table import HashTable
from package import Package


class Distances:
    """
    Creates a graph that stores in distances a tuple for each address. Each address has an ID based on where it is in excel.
    When retrieving the distance we can find out the distance to and from by checking if the destination is before or after the start
    as far as ID. This enables us to retrieve a distance to a location and back from a location relatively easily.
    """

    def __init__(self, file_path: str):
        self.graph = self.__get_distances_from_file(file_path)
        self.__set_distances()

    def __get_distances_from_file(self, file_path: str):
        try:
            distance_data = pd.read_excel(rf"{file_path}", skiprows=7)
            graph = [[0.0 for _ in range(distance_data.shape[0])] for _ in range(2, distance_data.shape[1])]
            for r in range(len(graph)):
                for c in range(len(graph[0])):
                    graph[r][c] = float(distance_data.iloc[r][c + 2])
            return graph
        except FileNotFoundError:
            raise FileNotFoundError("There is no excel file for the distances.") from None
        except ValueError:
            raise ValueError("The distances are not in a valid format.") from None

    def __set_distances(self):
        for r in range(len(self.graph)):
            for c in range(len(self.graph[0])):
                if math.isnan(self.graph[r][c]):
                    self.graph[r][c] = self.__get_distance_of_two_points(r, c)

    def __get_distance_of_two_points(self, start: int, destination: int):
        try:
            if destination > start:
                return self.graph[destination][start]
            else:
                return self.graph[start][destination]
        except IndexError:
            raise IndexError("Out of range start or destination.") from None

    """
    Greedy Algorithm to determine the minimum distance between each package stop.
    How it works:
    Parameters: A list of packages, and an address table that can link the address in the package to an ID in the address table.
    We use a tuple with three values, first is the distance as a float, second is the address ID of that destination
    that tells us where we are, and last is an index that tells us which package we selected.
    The min_distance tracks what's the minimum distance between each stop.
    We loop while they are still packages in the passed in packages array.
    We create a distance_options array so we can find out which package is the best option.
    We traverse through the packages and update distance options with a tuple that includes the distance from the
    start to the package's id, the address id of that package, and the index of that package.
    The new start is whatever option has the minimum distance.
    We add the new start's distance to min_distance.
    We remove the package from the packages list.
    """

    def get_min_distance(self, packages: list[Package], address_table:HashTable):
        start = (0, 0, 0)  # distance, address_id, index
        min_distance = 0.0
        while packages:
            distance_options = []
            for i in range(len(packages)):
                address_id = address_table.get(packages[i].address)
                distance_options.append((self.graph[start[1]][address_id], address_id, i))
            print(distance_options)
            start = min(distance_options, key=lambda x: x[0])
            min_distance += start[0]
            packages.pop(start[2])
        return min_distance

