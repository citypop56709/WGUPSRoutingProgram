"""
Class to help manage multiple trucks. This class has methods and attributes specifically for seeing where all the packages are.
"""
from address import Address
from hash_table import HashTable
from package import Package
from truck import Truck


class Depot:
    def __init__(self, address_list: list[list[int]], packages: HashTable):
        self.trucks = []
        self.packages = packages
        self.address_list = address_list
        self.delayed_packages = []
        self.deliverable_packages = []
    def process_packages(self) -> None:
        for package in self.packages.values():
            #if the package has no special notes it will go to truck3 where it will be taken by anyone
            if type(package.note) == str:
                #All the packages with a delayed arrival will be sent to the delayed packages list.
                if package.arrival:
                    self.delayed_packages.append(package)
                #If the package has a wrong address
                elif package.note == "Wrong address listed":
                    package.address = self.address_list[20]
                    self.delayed_packages.append(package)


    def load_trucks(self):
        truck1 = Truck(1, [], self.address_list)
        truck2 = Truck(2, [], self.address_list)