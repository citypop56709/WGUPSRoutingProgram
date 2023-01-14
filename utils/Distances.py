from collections import defaultdict
import pandas as pd


class Distances:
    """
    Creates a graph that stores in distances a tuple for each address. Each address has an ID based on where it is in excel.
    When retrieving the distance we can find out the distance to and from by checking if the destination is before or after the start
    as far as ID. This enables us to retrieve a distance to a location and back from a location relatively easily.
    """

    def __init__(self, file_path: str):
        self.graph = self.__get_distances(file_path)

    def __get_distances(self, file_path: str):
        try:
            distance_data = pd.read_excel(rf"{file_path}", skiprows=7)
            graph = [[j for j in range(2, len(distance_data.columns))] for i in range(len(distance_data))]
            R, C = len(graph), len(graph[0])
            for r in range(R):
                for c in range(C):
                    graph[r][c] = distance_data.iloc[r][c+2]
            return graph
        except FileNotFoundError:
            raise FileNotFoundError("There is no excel file for the distances.") from None
        except ValueError:
            raise ValueError("The distances are not in a valid format.") from None

    def get_distance(self, start: int, destination: int):
        try:
            if destination > start:
                return self.graph[destination][start]
            else:
                return self.graph[start][destination]
        except IndexError:
            raise IndexError("Out of range start or destination.") from None
