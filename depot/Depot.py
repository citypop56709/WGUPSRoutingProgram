"""
Class to help manage multiple trucks. This class has methods and attributes specifically for seeing where all the packages are.
"""
import datetime
from collections import deque
from hash_table import HashTable
from package import Package
from utils import config


class Depot:
    # This is static variable so that way it's easier for the Truck class to access.
    # The reason why it uses a deque is to make removing and appending the first item in a list much faster.
    delayed_packages = deque()
    available_deadline_packages = deque()
    available_for_pickup = []
    def __init__(self, address_list: list[list[int]], package_table: HashTable):
        self.trucks = []
        self.package_table = package_table
        self.address_list = address_list
        self.deliverable_packages = self.process_packages()
        self.total_mileage = None

    def process_packages(self) -> list[Package]:
        deliverable_packages = []
        for package in self.package_table.values():
            #if the package has no special notes it will go to truck3 where it will be taken by anyone
            if package.note:
                #All the packages with a delayed arrival will be sent to the delayed packages list.
                if package.arrival:
                    Depot.delayed_packages.append(package)
                #If the package has a wrong address
                elif package.note == "Wrong address listed" :
                    package.street_address = self.address_list[20]
                    package.arrival = datetime.datetime.now().replace(hour=10, minute=30)
                    Depot.delayed_packages.append(package)
                else:
                    deliverable_packages.append(package)
            else:
                deliverable_packages.append(package)
        return deliverable_packages

    def get_co_packages(self) -> list[Package]:
        packages = []
        removed_duplicate_packages = []
        for package in self.deliverable_packages:
            if package.co_package:
                for co_package in package.co_package:
                    if co_package not in packages:
                        packages.append(co_package)
                    if co_package.co_package:
                        for ex_package in co_package.co_package:
                            if ex_package not in packages:
                                packages.append(ex_package)
        for package in packages:
            if package not in removed_duplicate_packages:
                removed_duplicate_packages.append(package)
        return removed_duplicate_packages


    def load_trucks(self, truck=None):
        #Sort packages by closest to the hub to the farthest
        from truck import Truck
        self.deliverable_packages.sort(key=lambda x: x.address.distances[0])
        truck1_list = []
        truck2_list = []
        co_package_list = self.get_co_packages()
        for package in self.deliverable_packages:
            #Change the package to show it's in route if a user looks it up.
            package.status = "In Route"
            #Adds all the co-packages. It has to remove it from the list or else it would keep adding forever.
            if package in co_package_list:
                truck2_list.append(package)
                package.pickup_time = config.work_start_time
                package.truck = 2
                #We change the co-package attribute from a list to a boolean. Since they will all get delivered together.
                package.co_package = True
            elif package.deadline and package not in truck2_list and len(truck1_list) < 16:
                truck1_list.append(package)
                package.pickup_time = config.work_start_time
                package.truck = 1
            elif package.truck2 and len(truck2_list) < 16:
                truck2_list.append(package)
                package.pickup_time = config.work_start_time
                package.truck = 2
            elif len(truck1_list) < 16:
                if package not in truck2_list:
                    truck1_list.append(package)
                    package.pickup_time = config.work_start_time
                    package.truck = 1
            elif len(truck2_list) < 16:
                if package not in truck1_list:
                    truck2_list.append(package)
                    package.pickup_time = config.work_start_time
                    package.truck = 2
            else:
                if package.deadline:
                    Depot.available_deadline_packages.append(package)
                    print(f"The package {package.id} is a deadline package leftover")
                else:
                    Depot.available_for_pickup.append(package)
        self.trucks.append(Truck(1, truck1_list, self.address_list, self.package_table))
        self.trucks.append(Truck(2, truck2_list, self.address_list, self.package_table))

    #A function get the total miles for each truck.
    #
    def get_total_mileage(self) -> float:
        total_miles = 0.0
        for truck in self.trucks:
            total_miles += truck.get_total_miles()
        return total_miles
