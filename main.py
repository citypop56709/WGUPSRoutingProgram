from hash_table import HashTable
from package import Package
from collections import defaultdict
import pandas as pd


def main():
    hash_table = HashTable()
    package_data = pd.read_excel(r"Documentation/WGUPS Package File.xlsx", skiprows=7)
    for i in range(len(package_data)):
        values = package_data.iloc[i]
        new_package = Package(values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7])
    distance = defaultdict(list)
    get_distance()

"""
Creates a graph that stores in distances a tuple for each address. Each address has an ID based on where it is in excel.
When retreiving the distance we can find out the distance to and from by checking if the destination is before or after the start
as far as ID. This enables us to retrieve a distance to a location and back from a location relatively easily.
"""
def set_distance():
    distance_data = pd.read_excel(r"Documentation/WGUPS Distance Table.xlsx", skiprows=7)
    graph = defaultdict(tuple)
    address_id = 0
    for i in distance_data.columns[2:]:
        distance_values = distance_data[i].to_list()
        graph[address_id] = tuple(distance_values)
        address_id += 1
    destination = 0
    start = 26
    if destination < start:
        print(graph[destination][start])
    else:
        print(graph[start][destination])



if __name__ == '__main__':
    main()
