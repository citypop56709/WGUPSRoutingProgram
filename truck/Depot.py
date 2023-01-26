"""
Class to help manage multiple trucks. This class has methods and attributes specifically for seeing where all the packages are.
"""
import datetime
from hash_table import HashTable
from package import Package
from truck import Truck


class Depot:
    total_mileage = 0
    def __init__(self, address_list: list[list[int]], package_table: HashTable):
        self.trucks = []
        self.package_table = package_table
        self.address_list = address_list
        self.delayed_packages = []
        self.deliverable_packages = self.process_packages()
        self.work_start_time = self.get_work_start_time()

    def process_packages(self) -> list[Package]:
        deliverable_packages = []
        for package in self.package_table.values():
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
            #Change the package to show its in route if a user looks it up.
            package.status = "In Route"
            if package.co_package:
                #Add itself into truck2's list as a co_package
                if package not in truck2_list:
                    truck2_list.append(package)
                    #Add all potential co_packages to truck2's list.
                    for co_package_id in package.co_package:
                        package_in_co_package_list = self.package_table.get(co_package_id)
                        if package_in_co_package_list and package_in_co_package_list not in truck2_list:
                            truck2_list.append(package_in_co_package_list)
                            package_in_co_package_list.status = "In Route"
            elif package.truck2:
                truck2_list.append(package)
            elif len(truck1_list) < 16:
                truck1_list.append(package)
            elif len(truck2_list) < 16:
                truck2_list.append(package)
        self.trucks.append(Truck(1, truck1_list, self.address_list, self.package_table, self.work_start_time))
        self.trucks.append(Truck(2, truck2_list, self.address_list, self.package_table, self.work_start_time))

    def get_work_start_time(self):
        current_date = datetime.datetime.today()
        return current_date.replace(hour=8, minute=30, second=0)
