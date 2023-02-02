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
        self.next_stop_time = None
        self.status = "At Hub."

    #A function to go through all the current packages and make deliveries.
    def deliver_packages(self):
        while self.current_packages:

            distance = self.get_next_package_distance()
            if distance == float("inf"):
                break
            self.total_miles += distance
            self.update_package_delivery_info()
            self.current_package.status = "Delivered"
            self.truck_current_time = self.current_package.delivery_time
            if self.current_package in self.options:
                self.options.remove(self.current_package)
            if self.current_package in self.deadline_package_list:
                self.deadline_package_list.remove(self.current_package)
            if self.current_package in self.co_package_list:
                self.co_package_list.remove(self.current_package)
            self.current_packages.remove(self.current_package)
            if self.current_package.deadline:
                print(f"{self.current_package.delivery_info}, Package Deadline: {self.current_package.deadline}")
            else:
                print(self.current_package.delivery_info)
            if self.truck_id == 1:
                if self.process_delayed_packages(self.truck_current_time, distance):
                    self.return_to_hub()
                    self.deadline_package_list = self.process_deadline_packages()
                else:
                    pass
        if self.current_package:
            print(self.current_package.delivery_time)
        if not self.current_package:
            self.status = f"Current status of Truck {self.truck_id} at {self.truck_current_time} is at the hub."
            return
        else:
            self.status = "At hub"


    #A function that determines what the next package to be delivered should be.
    #Returns the distance of that package from the starting location.
    #Developer's Note: This function and the deliver_packages function used to be one thing.
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
        self.next_stop_time = self.get_time(self.truck_current_time, candidate_distance)
        self.current_package.delivery_time = self.next_stop_time
        return candidate_distance if not self.is_past_time_range(self.next_stop_time) else float("inf")

    #A function to update the delivery info so that it displays when the package was delivered.
    #It also changes the packages status to "Delivered"
    #The function also changes the truck's start time to match the new delivery time.
    def update_package_delivery_info(self) -> None:
        self.truck_current_time = self.next_stop_time
        self.current_package.status = 'Delivered'
        self.current_package.delivery_time = self.truck_current_time
        self.current_package.delivery_info =(f'Package ID: {self.current_package.id}, ' 
                                            f'Address: {self.current_package.address.street_address}:'
                                            f' Delivered at {self.current_package.delivery_time.strftime("%H:%M:%S")}')

    #A function to get the delivery time for a package.
    #It gets the time in hours as the distance divided by speed which is always 18 mph,
    #It returns new_time which is the start time that was originally inputted plus the additional time in hours.
    #This is separate to improve code re-use.
    def get_time(self, start_time: datetime, distance: float):
        time_h = distance/self.speed
        new_time = start_time + datetime.timedelta(hours=time_h)
        return new_time

    #A function to determine if a package is going to be past the global config time.
    #The point of this is to see if a package is already delivered or is currently on its way.
    def is_past_time_range(self, start_time: datetime) -> bool:
        return True if start_time >= config.current_time else False

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
        self.status = f"Truck {self.truck_id}: Returning to hub at {self.truck_current_time}."
        print(self.status)
        #We calculate the distance back to make sure to account for the time it takes to get back to the hub.
        distance_to_hub = self.current_package.address.distances[0]
        self.total_miles += distance_to_hub
        self.truck_current_time = self.get_time(self.truck_current_time, distance_to_hub)
        #If you don't set this to none the delivery won't be from the hub it will be from where that package was
        self.status = f"Truck {self.truck_id}: At Hub at {self.truck_current_time}"
        print(self.status)
        self.current_package = None

    def process_delayed_packages(self, start_time, distance) -> bool:
        picked_up = False
        arrival_time_to_hub = self.get_time(start_time, distance)
        #Loops through the delayed packages and separates packages that we can get whenever from packages that have to be retrieved now.
        for package in Depot.delayed_packages:
            #make sure we have no packages that MUST be delivered
            if package.arrival <= arrival_time_to_hub:
                #The program will always get packages with a deadline no matter what.
                if package.deadline:
                    Depot.available_deadline_packages.append(package)
                    Depot.delayed_packages.remove(package)
                else:
                    Depot.available_for_pickup.append(package)
                    Depot.delayed_packages.remove(package)
        #Do the logic here
        #Truck can only carry 16 packages at a time.
        if Depot.available_deadline_packages:
            #Pickup all the packages that have to be delivered no matter what.
            picked_up_deadline_packages = []
            for package in Depot.available_deadline_packages:
                print(f"The package ID at the Depot with a deadline is: {package.id} with deadline{package.deadline} and arrival of {package.arrival}")
            if self.deadline_package_list:
                if self.deadline_package_list[0].deadline >= Depot.available_deadline_packages[0].deadline:
                    return False
                else:
                    pass
            else:
                for package in Depot.available_deadline_packages:
                    print("We are now picking up packages from the Depot")
                    if len(self.current_packages) == 16:
                        break
                    else:
                        print(f"Picking up package with id {package.id}")
                        self.current_packages.append(package)
                        Depot.available_deadline_packages.remove(package)
                        picked_up = True
                        # If you don't remove them from the Depot packages then it will pick it up twice.
                #If there's room for more packages the truck can pick them up too.
                for package in Depot.available_for_pickup:
                    if len(self.current_packages) == 16:
                        break
                    else:
                        self.current_packages.append(package)
                        Depot.available_for_pickup.remove(package)
                        picked_up = True
            return picked_up

    #A function to get packages at the hub that may be leftover.
    #It returns a bool so the program can know if a pacakge was actually picked up or not.
    def get_leftover_packages(self) -> bool:
        picked_up = False
        for package in Depot.available_for_pickup:
            self.current_packages.append(package)
            Depot.available_for_pickup.remove(package)
            picked_up = True
        return picked_up


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

    #A function that returns a list of all the deadline packages in the current package list.
    def process_deadline_packages(self):
        deadline_package_list = []
        for package in self.current_packages:
            if package.deadline:
                deadline_package_list.append(package)
        return deadline_package_list

    #A function that returns all the non speciality packages in the current packages list.
    def process_packages(self):
        options = []
        for package in self.current_packages:
            if package not in self.co_package_list and package not in self.deadline_package_list:
                options.append(package)
        return options



