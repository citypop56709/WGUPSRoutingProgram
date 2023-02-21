import datetime

from address import Address
from depot import Depot
from package import Package
from utils import config

# A class to create a truck object representing a truck driver delivering the packages on a route.
class Truck:
    # A constructor for the truck class.
    # The class takes in an ID, to establish which truck this is, a packages list, which represents all the packages physically on the truck,
    # and it takes in an address list, which is a map of where the packages can be delivered.
    # The truck sorts the packages it has into three lists before it starts delivering anything: A list of co-packages,
    # a list of deadline packages, and a list of options e.g. a list of normal packages without any special conditions.
    # Note: In real life, this is what the truck drivers did at FedEx. They would go behind us and change up their packages slightly so packages
    # that had a strict deadline, like medical supplies, would ride with them up front.
    def __init__(self, truck_id, current_packages: list[Package],
                 address_list: list[Address]):
        self.truck_id = truck_id
        self.current_package = None  # The current address for the driver is partially based on the address of the current package.
        self.speed = float(18) # The driver's speed is fixed in this program.
        self.current_packages = current_packages
        self.address_list = address_list
        self.must_deliver_packages = []
        self.delayed_packages = []
        self.co_package_list = self.process_co_packages()
        self.deadline_package_list = self.process_deadline_packages()
        self.options = self.process_packages()
        self.truck_current_time = config.work_start_time
        self.total_miles = [(0.0, self.truck_current_time)]

    # A function to go through all the current packages and make deliveries.
    # This function works by first getting the distance to the next location using the get_next_package function.
    # Then it computes the time and mileage for that location to simulate driving there.
    # Then it removes the package that was delivered from all the package lists.
    # After the package is delivered the truck checks the packages back at the Depot to see if it is worth going back to grab more packages or carry on.
    # After all the packages possible are delivered the truck returns to the hub.
    # This function combined with the get_next_package function makes up the self-adjusting heuristic nearest-neighbor
    # algorithm that is detailed in section A in the readme.
    # Big O: O(n^2) - The time complexity of the nearest neighbor algorithm is O(n^2) because it has to perform the get_next_package function for each package,
    #                 and run the process_left_over_packages function for each package on the truck.
    def deliver_packages(self):
        while self.current_packages:
            next_location = self.get_next_package()
            self.truck_current_time = self.current_package.delivery_time
            self.total_miles.append((next_location+self.total_miles[-1][0], self.truck_current_time))
            if self.current_package in self.options:
                self.options.remove(self.current_package)
            if self.current_package in self.deadline_package_list:
                self.deadline_package_list.remove(self.current_package)
            if self.current_package in self.co_package_list:
                self.co_package_list.remove(self.current_package)
            self.current_packages.remove(self.current_package)
            if self.process_leftover_packages(self.truck_current_time, next_location):
                self.return_to_hub()
                self.options = self.process_packages() #If you do not do this then the options packages will not be properly updated.
                self.deadline_package_list = self.process_deadline_packages()
        else:
            self.return_to_hub()
        return

    # A function that determines what the next package to be delivered should be.
    # Returns the distance of that package from the starting location.
    # Fun fact: This function and the deliver_packages function used to be one thing. It was unwieldy to test, so they were separated.
    # How it works:
    # 1. The driver has a starting position, if the driver is just starting it will be the hub,
    #    otherwise the position will be represented by the address ID of the last delivered package.
    #    (Logically this makes sense, our driver has just made a delivery and is still there)
    # 2. The driver checks each package that is on the truck.
    # 3. Packages are sorted appropriately; deadline packages are sorted by their deadline, co-packages are sorted by distance,
    #    and non-special options packages are sorted by distance.
    # 4. If they are co-packages they are delivered first because they have to be delivered together.
    # 5. Otherwise, packages with deadlines are delivered first, and then the closest packages are delivered next.
    # 6. The selected package is known as "the candidate" the candidate becomes the new current package, and its address ID becomes the truck's new current location for the next delivery.
    # Big O: O(n log n) - The most time complex operation is sorting each list so that the function can check the first value in each one.
    def get_next_package(self) -> float:
        current_location = 0 if not self.current_package else self.current_package.address.id
        #Deadline packages are sorted by deadline.
        if self.deadline_package_list:
            self.sort_deadline_packages(current_location)
        #Co-packages are sorted by distance
        if self.co_package_list:
            self.co_package_list.sort(key=lambda x: x.address.distances[current_location])
        #Regular option packages are sorted by distance
        if self.options:
            self.options.sort(key=lambda x:x.address.distances[current_location])
        candidate = None
        candidate_distance = None
        #Co-packages always get chosen first because they have to be delivered together.
        if self.co_package_list:
            candidate = self.co_package_list[0]
            candidate_distance = candidate.address.distances[current_location]
        else:
            candidate = self.options[0] if self.options else None
            candidate_distance = candidate.address.distances[current_location] if candidate else None
            if self.deadline_package_list:
                deadline_package = self.deadline_package_list[0]
                #If the package in deadline list is the same as the current candidate then nothing needs to be done.
                if deadline_package == candidate:
                    pass
                #If they are deadline packages but no option packages then the next deadline package gets selected as the candidate.
                else:
                    candidate = deadline_package
                    candidate_distance = candidate.address.distances[current_location]
        self.current_package = candidate
        self.current_package.en_route_time = self.truck_current_time
        #The delivery time is calculated by adding the time it takes to get to the destination.
        self.current_package.delivery_time = self.get_time(self.truck_current_time, candidate_distance)
        return candidate_distance

    # A function to calculate the time it would take to travel to a certain distance.
    # It gets the time in hours as the distance divided by the speed which is always 18 mph.
    # This is separate to improve code reuse. This function is used often in the delivery process for many purposes.
    # Big O: O(1) - Constant time. There are no loops so creating the variable and calculating the time difference does take
    #               computing time is negligible compared to a loop.
    def get_time(self, start_time: datetime, distance: float):
        time_h = distance/self.speed
        new_time = start_time + datetime.timedelta(hours=time_h)
        return new_time

    # A function that sorts the packages with a deadline by how soon the deadline is.
    # If the packages all have the same deadline, then they are sorted by the distance from the truck's current location.
    # The truck's current location is represented by its index in the distances list.
    # Big O: O(n log n) - The time complexity is O(n log n) worst case because the packages have to be sorted which takes longer than
    #                     traversing through the for loop which is O(n) time complexity.
    def sort_deadline_packages(self, current_location: int):
        same_deadline = True
        first_package = self.deadline_package_list[0]
        for i in range(1, len(self.deadline_package_list)):
            if first_package.deadline != self.deadline_package_list[i]:
                same_deadline = False
                break
        if same_deadline:
            self.deadline_package_list.sort(key=lambda x:x.address.distances[current_location])
        else:
            self.deadline_package_list.sort(key=lambda x:x.deadline)

    # A function that checks each package on the truck and returns a list of all the co-packages.
    # This is possible due to the work done earlier in the Depot class to get a list of all the co-packages, and change
    # the co-package attribute to a boolean instead of a list.
    # Big O: O(n) - The function only has to loop though each package once to find the co-packages.
    def process_co_packages(self):
        co_packages = []
        for package in self.current_packages:
            if package.co_package:
                co_packages.append(package)
        return co_packages

    #A function that returns a list of all the packages with a deadline on the truck.
    # Big O: O(n) - The function only has to loop once to find which packages have a deadline or not.
    def process_deadline_packages(self):
        deadline_package_list = []
        for package in self.current_packages:
            if package.deadline:
                deadline_package_list.append(package)
        return deadline_package_list

    # A function that returns a list of non-speciality packages. These are packages that do not have co-packages, or a deadline.
    # Big O: O(n) The function only has to loop once to find which packages do not have special conditions.
    #             This function must be run after the process co_packages() and process_deadline_packages() functions.
    def process_packages(self):
        options = []
        for package in self.current_packages:
            if package not in self.co_package_list and package not in self.deadline_package_list:
                options.append(package)
        return options

    # The function represents a truck driver doing the following actions:
    # 1. The driver checks the delayed packages to see if any delayed packages have arrived.
    #    if those packages had deadlines they will get delivered first.
    # 2. The driver checks the packages with a deadline that are left over. If the first package that is already on the truck's deadline list
    #    has a deadline that is after the leftover package's deadline, then the driver does not go back to the hub. Why go back if you have a package with a more pressing need already?
    # 3. If the leftover package does have a deadline that is sooner than the soonest deadline on the truck, then the driver grabs as many
    # deadline packages as possible. If the driver has space, they will also get non-special leftover packages. The driver should grab as much as possible to reduce trips.
    # 4. If there are no deadlines on the truck or at the hub, then the driver will just grab as many packages as they can when it is convenient.
    # Note: In real life, this represents a driver physically going back to the hub, and looking around to decide what packages to get next.
    # Big O: O(n) - There are multiple loops but only one loop is run at a time restricting the time complexity to O(n), linear time.
    def process_leftover_packages(self, start_time, distance) -> bool:
        picked_up = False
        picked_up_packages = []
        arrival_time_to_hub = self.get_time(start_time, distance)
        # Loops through the delayed packages and separates packages that can be retrieved whenever from packages that have to be retrieved now.
        if Depot.delayed_packages:
            # The package cannot be moved from delayed if it has not arrived.
            if Depot.delayed_packages[0].arrival <= arrival_time_to_hub:
                # Packages with a deadline are moved to a separate list from those without one.
                while Depot.delayed_packages:
                    if Depot.delayed_packages[0].deadline:
                        Depot.available_deadline_packages.append(Depot.delayed_packages.popleft())
                    else:
                        Depot.available_for_pickup.append(Depot.delayed_packages.popleft())
        if Depot.available_deadline_packages:
            # First we check the deadline package list for this truck.
            # If the deadline on that package is before the one at the Depot then the driver does not return to the hub.
            if self.deadline_package_list:
                if self.deadline_package_list[0].deadline >= Depot.available_deadline_packages[0].deadline:
                    return False
                else:
                    pass
            # If there are deadline packages available for pickup, and it is possible to retrieve them then the driver will.
            # The package gets removed from all the Depot package lists it may be on, so that why the package is not duplicated.
            # The package is added to the truck's current packages list, and its deadline packages list.
            else:
                while Depot.available_deadline_packages and len(self.current_packages) < 16:
                    new_deadline_package = Depot.available_deadline_packages.popleft()
                    new_deadline_package.truck = self.truck_id
                    new_deadline_package.pickup_time = arrival_time_to_hub
                    picked_up_packages.append(new_deadline_package)
                    self.current_packages.append(new_deadline_package)
                    self.deadline_package_list.append(new_deadline_package)
                    picked_up = True
        else:
            #If there are leftover packages at the depot then the driver will pick them up.
            for package in Depot.available_for_pickup:
                if package.truck2 and self.truck_id != 2:
                    pass
                else:
                    package.pickup_time = arrival_time_to_hub
                    package.truck = self.truck_id
                    picked_up_packages.append(package)
                    self.current_packages.append(package)
                    # You have to remove it here because it's not getting popped.
                    Depot.available_for_pickup.remove(package)
                    picked_up = True
        return picked_up

    # A function that process the mileage and time for the truck returning to the hub from its current location.
    # If the driver is already at the hub it returns from the function; Can't go back if you're already there.
    # Big O: O(1) - The operations in the function do take time, but the time is negligible compared to how much time it takes to traverse a loop, for example.
    def return_to_hub(self):
        if not self.current_package:
            return
        #We calculate the distance back to make sure to account for the time it takes to get back to the hub.
        distance_to_hub = self.current_package.address.distances[0]
        self.truck_current_time = self.get_time(self.truck_current_time, distance_to_hub)
        self.total_miles.append((distance_to_hub+self.total_miles[-1][0], self.truck_current_time))
        self.current_package = None

    #A function to get the current miles at a given time.
    #This works by looping through the tuples in the total miles list.
    #If the last time is greater than the current time then the previous index's mileage is the new total.
    #Time Complexity: O(n) worst case if it has to loop through each value.
    def get_total_miles(self, time: datetime) -> float:
        total = 0.0
        for i in range(len(self.total_miles)):
            if self.total_miles[i][1] > time:
                if i-1 >= 0:
                    total = self.total_miles[i-1][0]
                    return total
                else:
                    total = self.total_miles[0][0]
                    return total
            else:
                total = self.total_miles[i][0]
        return total


