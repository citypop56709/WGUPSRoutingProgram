from hash_table import HashTable
import pandas as pd
from hash_table import HashTable
from package import Package


class PackageList:

    @staticmethod
    def get_packages(file_path: str, address_table: HashTable):
        #starts at one to make matching packages with ID easier
        packages = []
        package_data = pd.read_excel(rf"{file_path}", skiprows=7)
        for i in range(package_data.shape[0]):
            values = package_data.iloc[i]
            new_package = Package(values[0], values[1], values[2], values[3], values[4], values[5], values[6],
                                  values[7])
            packages.append(new_package)
        return packages
