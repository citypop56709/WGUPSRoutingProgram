import datetime
from collections import deque

from address import Address
from hash_table import HashTable
from package import Package
from utils import config

# A Class to help manage multiple trucks.
# Note: This class was inspired by my time as a package handler at FedEx. We worked in a manner similar to this function:
# we processed and sorted each package, then we loaded them unto the correct trucks after
class Depot:
    # Note: delayed_packages, available_deadline_packages, and available_for_pickup are static variables because it makes it easier for the trucks to access them.
    # A deque is used with delayed_packages, and available_deadline_packages to make removing and appending values to the front of the list much faster.
    delayed_packages = deque()
    available_deadline_packages = deque()
    available_for_pickup = []

    # A constructor for the Depot class.
    # The constructor uses the package hash table, and the address list to create class attributes that can be used to load the trucks.
    # The deliverable_packages list is update as the packages are processed. The total_mileage attribute calculates the total mileage for all the trucks.
    def __init__(self, address_list: list[Address], package_table: HashTable):
        self.trucks = []
        self.package_table = package_table
        self.address_list = address_list
        self.deliverable_packages = self.process_packages()
        self.total_mileage = None

    # A function that processes each package in the packages hash table and returns a list of deliverable packages.
    # A package is deliverable if it is currently at the hub. Delayed packages are added to a delayed packages list
    # that is a class attribute. This function is called when the depot is constructed.
    # This allows it to get the packages it needs to start loading the trucks.
    # Big O: O(n^2) - The time complexity is O(n^2) because the function calls the values() function on the packages hash table.
    # The values() function has a time complexity pf O(n^2) so even though the for loop is O(n) to iterate through each package, the overall time complexity is still O(n^2).
    def process_packages(self) -> list[Package]:
        deliverable_packages = []
        for package in self.package_table.values():
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

    # A function to extract a list of co-packages from a package that has co-packages.
    # Big O: O(n^3) - The reason why the time complexity is O(n^3) is that the function has to check deliverable package
    # to see if it has co-packages, then it has to check co-package in that package's co-package list to if they have co-packages.
    # After that, it still has to loop one more time to see if those co-packages also have co-packages.
    # Note: The reason why this is so complex is that data is missing from some co-packages. So, the only way to get a full picture
    # is to loop tediously through each possible combination. If I didn't have to use my own hash table, I would have used a defaultdict
    # to implement a topological sort to get all the co-packages. Time did not allow this kind of experimentation.
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

    # A function to load packages onto each truck.
    # The function works by sorting each deliverable package by distance and then checking each package to load them onto the correct truck.
    # Certain packages have special conditions e.g. some packages can only be delivered using truck 2. These special conditions have to be processed
    # so that the packages are delivered on time and using the correct truck.
    # Big O: O(n^3) - The most time complex portion of the function is retrieving all the co-packages using the get_co_packages function.
    # The next most time complex portion is sorting each package by distance from the hub. The Python built-in sorting algorithm
    # has a time complexity of O(n log n). The for loop that occurs after the packages are sorted has a time complexity of O(n).
    def load_trucks(self):
        from truck import Truck
        self.deliverable_packages.sort(key=lambda x: x.address.distances[0]) #The function uses a lambda expression to sort packages by distance from the hub.
        truck1_list = []
        truck2_list = []
        co_package_list = self.get_co_packages()
        for package in self.deliverable_packages:
            if package in co_package_list:
                truck2_list.append(package)
                package.pickup_time = config.work_start_time #This time is changed to show that the package was picked up by a truck.
                package.truck = 2
                package.co_package = True #The co-packages attribute is changed to a boolean to show that it is a co-package.
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
                #If they are packages that are do not fit on any truck they are added to available_deadline_packages if they have a deadline,
                # and available_for_pickup if they do not.
                if package.deadline:
                    Depot.available_deadline_packages.append(package)
                else:
                    Depot.available_for_pickup.append(package)
        #After the truck lists are loaded, the function creates a truck object using that information.
        self.trucks.append(Truck(1, truck1_list, self.address_list))
        self.trucks.append(Truck(2, truck2_list, self.address_list))

    # A function get the total miles traveled for each truck.
    # Big O: O(n^2) - The time complexity is O(n^2) because the for loop has to iterate through each truck which is an O(n) operation,
    # and then call the get_total_miles function on each truck; also an O(n) operation.
    def get_total_mileage(self, time:datetime) -> float:
        total_miles = 0.0
        for truck in self.trucks:
            total_miles += truck.get_total_miles(time)
        return total_miles
