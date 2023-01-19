from typing import Optional

from hash_table import HashTable
from package import Package
from utils import Distances
from hash_table import HashTable


class Truck:
    def __init__(self, id, current_packages: list[Package], address_list: list[list[int]]):
        self.id = id
        self.current_package = None  # Current address
        self.speed = float(18)
        self.current_packages = current_packages
        self.address_list = address_list

    def deliver_packages(self):
        total_distance = 0.0
        while self.current_packages:
            min_distance, self.current_package = self.get_min_distance_package(self.current_package)
            total_distance += min_distance
            print(f'{self.current_package.address}: Minimum distance:{min_distance}: Total: {total_distance}')


    def get_min_distance_package(self, current_package:Optional[Package]) -> (float, Package):
        #you have a start which is based on the distance array
        #check each package's distance in that array from the start
        #whatever package is the minimum
        #return the distance
        #return the package
        start = 0 if not current_package else current_package.address.id
        options = []
        for package in self.current_packages:
            options.append((self.address_list[start][package.address.id], package))
        res = min(options, key=lambda x:x[0])
        self.current_packages.remove(res[1])
        return res

