from hash_table import HashTable
import pandas as pd

"""
This class contains a static method that makes a HashTable that associates the addresses from the excel spreadsheet
with the appropriate index in the distance 2D matrix. The point of this is so that we can work with integers
for all the operations and output the address for the display.

It works by creating a HashTable, reading the addresses from a pandas dataframe, and then using a for loop
to put each address into hashtable in the range of the 2D matrix.
"""


class AddressTable:
    @staticmethod
    def get_addresses(file_path: str, address_index: int):
        addresses = HashTable()
        address_data = pd.read_excel(rf"{file_path}", skiprows=7)
        address_list = address_data[address_data.columns[0]]
        for i in range(address_index):
            addresses.put(i, address_list[i])
        return addresses
