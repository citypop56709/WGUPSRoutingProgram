from hash_table import HashTable
import pandas as pd
from hash_table import HashTable
from package import Package

"""
This class has only one method, get_packages that retreives all the packages from the excel spreadsheet using Pandas
and places them into a hash table. It uses the package ID has a key and the package as a value. This makes it easy to lookup
package info.
"""


class PackageTable:

    @classmethod
    def get_packages(cls, file_path: str):
        packages_table = HashTable()
        package_data = pd.read_excel(rf"{file_path}", skiprows=7)
        for i in range(package_data.shape[0]):
            values = package_data.iloc[i]
            new_package = Package(values[0], values[1], values[2], values[3], values[4], values[5], values[6],
                                  values[7])
            packages_table.put(new_package.id, new_package)
        return packages_table
