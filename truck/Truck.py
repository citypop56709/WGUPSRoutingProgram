import datetime
from typing import Optional
from package import Package
from collections import deque

class Truck:
    def __init__(self, id, current_packages: Optional[list[Package]], address_list: list[list[int]], start_time: datetime, total_co_packages = 0):
        self.id = id
        self.current_package = None  # Current address
        self.speed = float(18)
        self.current_packages = current_packages
        self.address_list = address_list
        self.co_packages = total_co_packages
        self.co_package_queue = deque()
        self.time_to_deliver = None
        self.start_time = start_time

    def deliver_packages(self):
        total_distance = 0.0
        if self.current_packages:
            min_distance, self.current_package = self.get_min_distance_package()
            total_distance += min_distance
            print(f'{self.current_package.address.street_address}: Minimum distance:{min_distance}: Total: {total_distance}')
        else:
            total_distance += self.current_package.address.distances[0]
            print(f"Going back to hub: {total_distance}")

    def get_min_distance_package(self) -> (float, Package):
        #you have a start which is based on the distance array
        #check each package's distance in that array from the start
        #whatever package is the minimum
        #return the package
        start = 0 if not self.current_package else self.current_package.address.id
        options = []
        res = None
        for package in self.current_packages:
            #co-packages get added to a queue and then delivered after.
            if package.co_package and package.co_package not in self.co_package_queue:
                self.co_package_queue.append(package)
            else:
                options.append(package)
        #if there are packages in the co-package queue they get delivered first.
        if self.co_package_queue and len(self.co_package_queue) == self.co_packages:
            #res = self.co_package_queue.popleft()
            print(self.co_package_queue)
            res = self.co_package_queue.popleft()
            print(f'Adding the co_package: {self.current_package.id}')
        else:
            res = min(options, key=lambda x:x.address.distances[start])
        print(res)
        self.current_packages.remove(res)
        return res.address.distances[start], res

    def time_to_deliver(self, distance):
        time_h = distance/self.speed
        return self.start_time.replace()