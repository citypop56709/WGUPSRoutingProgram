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
        self.total_miles = 0.0

    #If there is no selected package then deliver the next otherwise deliver THIS ONE.
    def deliver_package(self, select_package=None, distance=0):
        if self.current_packages:
            self.current_package = select_package
            #If you do not pass in the distance first then what happens is that it creates an infinite loop.
            if not distance:
                distance = self.get_next_package_distance()
            self.total_miles += distance
            print(self.current_package.id)
            self.current_packages.remove(self.current_package)
            self.update_package_delivery_info(distance)
            self.current_package.status = "Delivered"
            print(self.current_package.delivery_info)
            #Check for co packages and delivers those too
            if self.current_package.co_package:
                self.process_copackages(self.current_package, distance)
        else:
            self.total_miles += self.current_package.address.distances[0]
            print(f"Going back to hub: {self.total_miles}")
    def process_copackages(self, package, distance):
        for co_package_id in package.co_package:
            #If a package is co_package it will get delivered and then all it's co packages will get automatically delivered.
            co_package = self.package_table.get(co_package_id)
            #If the co package is not None then we deliver it if it's in current packages. #Can't deliver whats done already.
            if co_package and co_package in self.current_packages:
                print(f"Processing co packages method is delivering package: {co_package}")
                self.deliver_package(co_package, distance)

    #A function that determines what the next package to be delivered should be.
    #Returns the distance of that package from the starting location.
    def get_next_package_distance(self) -> float:
        start = 0 if not self.current_package else self.current_package.address.id
        options = []
        for package in self.current_packages:
            #If a package is co_package it will get delivered
            #Then all it's co packages will get automatically delivered.
            if package.co_package and package in self.current_packages:
                distance_from_start = package.address.distances[start]
                print(f"Delivering package: {package.id}")
                self.deliver_package(package, distance_from_start)
            else:
                options.append(package)
        self.current_package = min(options, key=lambda x:x.address.distances[start])
        print(f"Now i am delivering in the get_next_package_distance method package id: {self.current_package.id}")
        return self.current_package.address.distances[start]

    #A function to update the delivery info so that it displays when the package was delivered.
    #It also changes the packages status to "Delivered"
    #The function also changes the truck's start time to match the deli
    def update_package_delivery_info(self, distance) -> None:
        time_h = distance/self.speed
        self.truck_current_time += datetime.timedelta(hours=time_h)
        self.current_package.status = 'Delivered'
        self.current_package.delivery_info =(f'Package ID: {self.current_package.id},' 
                                            f'Address: {self.current_package.address.street_address}',
                                            f'{self.truck_current_time.strftime("%H:%M:%S")}')


