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
        self.deliverable_packages = self.process_packages()

    def process_packages(self) -> list[Package]:
        deliverable_packages = []
        for package in self.packages.values():
            #if the package has no special notes it will go to truck3 where it will be taken by anyone
            if package.note:
                #All the packages with a delayed arrival will be sent to the delayed packages list.
                if package.arrival:
                    self.delayed_packages.append(package)
                #If the package has a wrong address
                elif package.note == "Wrong address listed":
                    package.street_address = self.address_list[20]
                    self.delayed_packages.append(package)
                else:
                    deliverable_packages.append(package)
            else:
                deliverable_packages.append(package)
        return deliverable_packages
        #change the class to deliver the delayed packages

    def load_trucks(self):
        truck1_list = []
        truck2_list = []
        #Sort packages by closest to the hub to the farthest
        self.deliverable_packages.sort(key=lambda x: x.address.distances[0])
        for package in self.deliverable_packages:
            if package.co_package:
                truck2_list.append(package)
            elif package.truck2:
                truck2_list.append(package)
            elif len(truck1_list) < 16:
                truck1_list.append(package)
            elif len(truck2_list) < 16:
                truck2_list.append(package)
        self.trucks.append(Truck(1, truck1_list, self.address_list))
        self.trucks.append(Truck(2, truck2_list, self.address_list))
