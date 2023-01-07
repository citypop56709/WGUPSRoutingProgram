from hash_table import HashTable
from package import Package
import pandas as pd


def main():
    hash_table = HashTable()
    data = pd.read_excel(r"Documentation/WGUPS Package File.xlsx", skiprows=7)
    for i in range(len(data)):
        values = data.iloc[i]
        new_package = Package(values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7])





if __name__ == '__main__':
    main()
