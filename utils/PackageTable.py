from hash_table import HashTable
from package import Package
import csv

"""
This class has only one method, get_packages that retreives all the packages from the excel spreadsheet using Pandas
and places them into a hash table. It uses the package ID has a key and the package as a value. This makes it easy to lookup
package info.
"""


class PackageTable:

    @classmethod
    def get_packages(cls, file_path: str, address_table: HashTable):
        packages_table = HashTable()
        file = open(file_path)
        package_data = csv.reader(file)
        for i, row in enumerate(package_data):
            if i > 7:
                values = row
                new_package = Package(values[0], address_table.get(values[1]), values[2], values[3], values[4], values[5], values[6],
                                      values[7])
                packages_table.put(new_package.id, new_package)
        return packages_table
