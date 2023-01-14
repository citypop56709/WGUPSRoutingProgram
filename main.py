from hash_table import HashTable
from package import Package
from utils import Distances
from collections import defaultdict
import pandas as pd


def main():
    hash_table = HashTable()
    package_data = pd.read_excel(r"Documentation/WGUPS Package File.xlsx", skiprows=7)
    print(len(package_data.columns))
    for i in range(len(package_data)):
        values = package_data.iloc[i]
        new_package = Package(values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7])
    distances = Distances(r"Documentation/WGUPS Distance Table.xlsx")
    print(distances.get_distance(6, 2))









if __name__ == '__main__':
    main()
