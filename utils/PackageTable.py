from hash_table import HashTable
import pandas as pd


class PackageTable:
    @staticmethod
    def get_packages(file_path: str):
        addresses = HashTable()
        package_data = pd.read_excel(rf"{file_path}", skiprows=7)
        package_list = package_data[package_data.columns[0]]
        for i in range(add):
            addresses.put(i, address_list[i])
        return addresses