import datetime
from typing import Optional

from hash_table import HashTable
from package import Package
from collections import deque

class Truck:
    def __init__(self, truck_id, current_packages: Optional[list[Package]],
                 address_list: list[list[int]], package_table: HashTable,
                 start_time: datetime):
        self.id = truck_id
        self.current_package = None  # Current address
        self.speed = float(18)
        self.current_packages = current_packages
        self.address_list = address_list
        self.package_table = package_table
        self.truck_current_time = start_time
        self.co_package_list = self.process_co_packages()
        self.deadline_package_list = self.process_deadline_packages()
        self.options = self.process_packages()
        self.total_miles = 0.0

    #If there is no selected package then deliver the next otherwise deliver THIS ONE.
    def deliver_package(self):
        if self.current_packages:
            distance = self.get_next_package_distance()
            self.total_miles += distance
            self.update_package_delivery_info(distance)
            self.current_package.status = "Delivered"
            if self.current_package.deadline:
                print(f"{self.current_package.delivery_info}, Deadline: {self.current_package.deadline}")
            else:
                print(self.current_package.delivery_info)
            if not self.current_packages:
                self.total_miles += self.current_package.address.distances[0]
                print(f"Going back to hub: {self.total_miles}")

    #A function that returns a list of all the co packages on this truck.
    #The reason why this is separate is to improve consistency. If there was one master list there won't be co-packages that are forgotten about.
    #Time Complexity: O(n*m) where n is the number of packages in current_packages and m is the number of co_packages in each package's co_package list.
    def process_co_packages(self) -> list[Package]:
        total_co_packages = set()
        for package in self.current_packages:
            if package.co_package:
                for co_package in package.co_package:
                    if co_package not in total_co_packages and co_package in self.current_packages:
                        total_co_packages.add(co_package)
        return list(total_co_packages)

    def process_deadline_packages(self):
        deadline_package_list = []
        for package in self.current_packages:
            if package.deadline:
                deadline_package_list.append(package)
        return deadline_package_list

    def process_packages(self):
        options = []
        for package in self.current_packages:
            if package not in self.co_package_list and package not in self.deadline_package_list:
                options.append(package)
        return options


    #A function that determines what the next package to be delivered should be.
    #Returns the distance of that package from the starting location.
    def get_next_package_distance(self) -> float:
        start = 0 if not self.current_package else self.current_package.address.id
        if self.deadline_package_list:
            self.sort_deadline_packages(start)
        if self.co_package_list:
            self.co_package_list.sort(key=lambda x: x.address.distances[start])
        if self.options:
            self.options.sort(key=lambda x:x.address.distances[start])

        candidate = None
        candidate_distance = None
        candidate_time = None
        index = 0
        if self.co_package_list:
            print(f"There is a candidate with {self.co_package_list[0]}")
            candidate = self.co_package_list[0]
            candidate_distance = candidate.address.distances[start]
            candidate_time = self.get_delivery_time(candidate, self.truck_current_time, candidate_distance)
        else:
            #If the candidate list is properly sorted the candidate is always going to be the first option in the list.
            candidate = self.options[0] if self.options else None
            candidate_distance = candidate.address.distances[start] if candidate else None
        if self.deadline_package_list:
            deadline_package = self.deadline_package_list[0]
            #If the package with the closest deadline is the same as the co-package then we leave the if statement.
            if deadline_package == candidate:
                pass
            #This statement is for the rare case when they are only deadline packages left and no regular packages.
            else:
                candidate = deadline_package
                candidate_distance = candidate.address.distances[start]
            """
            else:
                #This is the time that the Truck will be at if it delivers the potential candidate package
                candidate_time = self.get_delivery_time(candidate, self.truck_current_time, candidate_distance)
                #This is the distance of the deadline package from the candidate. We need this to calculate potential delivery time.
                distance_of_deadline_package_from_candidate = deadline_package.address.distances[candidate.address.id]
                #If a package would be late if we did not choose it then we have to choose it.

                if self.is_late(deadline_package, candidate_time, distance_of_deadline_package_from_candidate):
                    candidate = deadline_package
                    candidate_distance = candidate.address.distances[start]
            """
        if candidate in self.options:
            self.options.remove(candidate)
        if candidate in self.deadline_package_list:
            self.deadline_package_list.remove(candidate)
        if candidate in self.co_package_list:
            self.co_package_list.remove(candidate)
        self.current_packages.remove(candidate)
        self.current_package = candidate
        return candidate_distance

    #A function to update the delivery info so that it displays when the package was delivered.
    #It also changes the packages status to "Delivered"
    #The function also changes the truck's start time to match the deli
    def update_package_delivery_info(self, distance) -> None:
        self.truck_current_time = self.get_delivery_time(self.current_package, self.truck_current_time, distance)
        self.current_package.status = 'Delivered'
        self.current_package.delivery_info =(f'Package ID: {self.current_package.id},' 
                                            f'Address: {self.current_package.address.street_address}',
                                            f'{self.truck_current_time.strftime("%H:%M:%S")}')

    #A function to get the delivery time for a package.
    #This is separate to improve code re-use.
    def get_delivery_time(self, package: Package, start_time: datetime, distance: float):
        time_h = distance/self.speed
        new_time = start_time + datetime.timedelta(hours=time_h)
        return new_time

    #A function to see if a package would be late if we delivered another package FIRST.
    #The point of this is to make intelligent decisions about which package to deliver first.
    def is_late(self,  deadline_package : Package, start_time: datetime, distance: float):
        timeframe = self.get_delivery_time(deadline_package, start_time, distance)
        print(f"The timeframe is: {timeframe}")
        if timeframe >= deadline_package.deadline:
            return True
        else:
            return False

    def sort_deadline_packages(self, start: int):
        same_deadline = True
        first_package = self.deadline_package_list[0]
        for i in range(1, len(self.deadline_package_list)):
            if first_package.deadline != self.deadline_package_list[i]:
                same_deadline = False
                break
        if same_deadline:
            self.deadline_package_list.sort(key=lambda x:x.address.distances[start])
        else:
            self.deadline_package_list.sort(key=lambda x:x.deadline)




