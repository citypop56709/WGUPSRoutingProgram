from collections import defaultdict, deque

from hash_table import HashTable
from package import Package
from utils import AddressTable, Distances
import pandas as pd


def main():
    package_data = pd.read_excel(r"Documentation/WGUPS Package File.xlsx", skiprows=7)
    for i in range(len(package_data)):
        values = package_data.iloc[i]
        new_package = Package(values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7])
    distances = Distances(r"Documentation/WGUPS Distance Table.xlsx")
    #print(distances.graph[6][2])
    address_table = AddressTable.get_addresses(r"Documentation/WGUPS Distance Table.xlsx", len(distances.graph))
    print(address_table.get(1))
    distances_graph = defaultdict(list)












if __name__ == '__main__':
    main()
