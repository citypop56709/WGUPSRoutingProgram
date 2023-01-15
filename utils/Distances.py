import math
from collections import deque
import numpy as np
import pandas as pd


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
