import datetime

from depot import Depot
from hash_table import HashTable
from package import Package
from utils import config

class Truck:
    def __init__(self, truck_id, current_packages: list[Package],
                 address_list: list[list[int]], package_table: HashTable):
        self.truck_id = truck_id
        self.current_package = None  # Current address
        self.speed = float(18)
        self.current_packages = current_packages
        self.address_list = address_list
        self.package_table = package_table
        self.must_deliver_packages = []
        self.delayed_packages = []
        self.co_package_list = self.process_co_packages()
        self.deadline_package_list = self.process_deadline_packages()
        self.options = self.process_packages()
        self.total_miles = 0.0
        self.truck_current_time = config.start_time

    #A function to go through all the current packages and make deliveries.
    def deliver_packages(self):
        while self.current_packages:
            distance = self.get_next_package_distance()
            self.total_miles += distance
            self.truck_current_time = self.current_package.delivery_time
            if self.current_package in self.options:
                self.options.remove(self.current_package)
            if self.current_package in self.deadline_package_list:
                self.deadline_package_list.remove(self.current_package)
            if self.current_package in self.co_package_list:
                self.co_package_list.remove(self.current_package)
            self.current_packages.remove(self.current_package)
            if self.process_leftover_packages(self.truck_current_time, distance):
                self.return_to_hub()
                self.options = self.process_packages() #If you do not do this then the options packages will not be properly updated.
                self.deadline_package_list = self.process_deadline_packages()
        else:
            self.return_to_hub()
            config.total_mileage += self.total_miles
        return


    #A function that determines what the next package to be delivered should be.
    #Returns the distance of that package from the starting location.
    #Developer's Note: This function and the deliver_packages function used to be one thing.
    def get_next_package_distance(self) -> float:
        start = 0 if not self.current_package else self.current_package.address.id
        #Deadline packages are sorted by deadline.
        if self.deadline_package_list:
            self.sort_deadline_packages(start)
        #Co-packages are sorted by distance
        if self.co_package_list:
            self.co_package_list.sort(key=lambda x: x.address.distances[start])
        #Regular options are sorted by distance
        if self.options:
            self.options.sort(key=lambda x:x.address.distances[start])
        candidate = None
        candidate_distance = None
        #Co-packages always get chosen first because they have to be delivered together.
        if self.co_package_list:
            candidate = self.co_package_list[0]
            candidate_distance = candidate.address.distances[start]
        else:
            #If the candidate list is properly sorted the candidate is always going to be the first option in the list.
            candidate = self.options[0] if self.options else None
            candidate_distance = candidate.address.distances[start] if candidate else None
            if self.deadline_package_list:
                deadline_package = self.deadline_package_list[0]
                #If the package in deadline list is the same as the co-package then we leave the if statement.
                if deadline_package == candidate:
                    pass
                #This statement is for the rare case when they are only deadline packages left and no regular packages.
                else:
                    candidate = deadline_package
                    candidate_distance = candidate.address.distances[start]
        self.current_package = candidate
        #The time that is en-route is the current time
        self.current_package.en_route_time = self.truck_current_time
        #The delivery time is calculated by adding the time it takes to actually get to the destination.
        self.current_package.delivery_time = self.get_time(self.truck_current_time, candidate_distance)
        return candidate_distance

    #A function to get the delivery time for a package.
    #It gets the time in hours as the distance divided by speed which is always 18 mph,
    #It returns new_time which is the start time that was originally inputted plus the additional time in hours.
    #This is separate to improve code re-use.
    def get_time(self, start_time: datetime, distance: float):
        time_h = distance/self.speed
        new_time = start_time + datetime.timedelta(hours=time_h)
        return new_time

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

    def return_to_hub(self):
        if not self.current_package:
            return
        #We calculate the distance back to make sure to account for the time it takes to get back to the hub.
        distance_to_hub = self.current_package.address.distances[0]
        self.total_miles += distance_to_hub
        self.current_package = None
        self.truck_current_time = self.get_time(self.truck_current_time, distance_to_hub)

    def process_leftover_packages(self, start_time, distance) -> bool:
        picked_up = False
        picked_up_packages = []
        arrival_time_to_hub = self.get_time(start_time, distance)
        #Loops through the delayed packages and separates packages that we can get whenever from packages that have to be retrieved now.
        if Depot.delayed_packages:
            #We can't move the package from delayed unless it's actually arrived.
            if Depot.delayed_packages[0].arrival <= arrival_time_to_hub:
                #The program will always get packages with a deadline no matter what.
                while Depot.delayed_packages:
                    if Depot.delayed_packages[0].deadline:
                        Depot.available_deadline_packages.append(Depot.delayed_packages.popleft())
                    else:
                        Depot.available_for_pickup.append(Depot.delayed_packages.popleft())
            else:
                return
        if Depot.available_deadline_packages:
            #First we check the deadline package list for this truck. If the deadline on that package is before the one in the Depot we don't go back until it's delivered.
            if self.deadline_package_list:
                if self.deadline_package_list[0].deadline >= Depot.available_deadline_packages[0].deadline:
                    return False
                else:
                    pass
            #If there either are no deadline packages or the deadline of the Depot package is before the current deadline package we add it to our list.
            else:
                while Depot.available_deadline_packages and len(self.current_packages) < 16:
                    new_deadline_package = Depot.available_deadline_packages.popleft()
                    new_deadline_package.truck = self.truck_id
                    new_deadline_package.pickup_time = arrival_time_to_hub
                    picked_up_packages.append(new_deadline_package)
                    self.current_packages.append(new_deadline_package)
                    self.deadline_package_list.append(new_deadline_package)
                    picked_up = True
                #Loop has to change because available_for_pickup is a list not a deque.
        else:
            for package in Depot.available_for_pickup:
                if package.truck2 and self.truck_id != 2:
                    pass
                else:
                    package.pickup_time = arrival_time_to_hub
                    package.truck = self.truck_id
                    picked_up_packages.append(package)
                    self.current_packages.append(package)
                    #You have to remove it here because it's not getting popped.
                    Depot.available_for_pickup.remove(package)
                    picked_up = True
        return picked_up

    #A function that returns a list of all the deadline packages in the current package list.
    def process_deadline_packages(self):
        deadline_package_list = []
        for package in self.current_packages:
            if package.deadline:
                deadline_package_list.append(package)
        return deadline_package_list

    def process_co_packages(self):
        co_packages = []
        for package in self.current_packages:
            if package.co_package:
                co_packages.append(package)
        return co_packages

    #A function that returns all the non speciality packages in the current packages list.
    def process_packages(self):
        options = []
        for package in self.current_packages:
            if package not in self.co_package_list and package not in self.deadline_package_list:
                options.append(package)
        return options



