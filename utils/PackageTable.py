import datetime
from typing import Optional
from hash_table import HashTable
from utils import config
import csv

class PackageTable(HashTable):

    # A function to get the current status of a package given a specific time.
    # This tells you where that package was.
    # It works by checking the time compared to each stage of the package and then sets the status to a string.
    # The program uses tuples to make sorting by package status simple.
    def package_lookup(self, id: int):
        package = self.get(id)
        status_info = None
        if package.pickup_time > config.current_time and package.arrival:
            package.status = (0, "Delayed")
            time_string = datetime.datetime.strftime(package.arrival, "%H:%M %p")
            status_info = f"Package {package.id}, Address: {package.address.street_address}, {package.city}, {package.zip}, Weight: {package.mass}, Status: {package.status[1]} arriving at {time_string}"
            package.status_change = True if package.status != package.last_status else False
            package.last_status = package.status
            return status_info
        if package.pickup_time > config.current_time and not package.arrival:
            package.status = (1, "At Hub")
            status_info = (f"Package {package.id}, Address: {package.address.street_address}, {package.city}, {package.zip}, Weight: {package.mass}, Status: {package.status[1]}")
            package.status_change = True if package.status != package.last_status else False
            package.last_status = package.status
            return status_info
        elif package.en_route_time > config.current_time:
            package.status = (2, "Picked Up")
            time_string = datetime.datetime.strftime(package.pickup_time, "%H:%M %p")
            status_info = (
                f"Package {package.id}, Address: {package.address.street_address}, {package.city}, {package.zip}, Weight: {package.mass}, Status: {package.status[1]} at {time_string}, Truck: {package.truck}")
        elif package.delivery_time > config.current_time:
            package.status = (3, "En Route")
            time_string = datetime.datetime.strftime(package.en_route_time, "%H:%M %p")
            status_info = (
                f"Package {package.id}, Address: {package.address.street_address}, {package.city}, {package.zip}, Weight: {package.mass}, Status: {package.status[1]} at {time_string}, Truck: {package.truck}")
        else:
            package.status = (4, "Delivered")
            time_string = datetime.datetime.strftime(package.delivery_time, "%H:%M %p")
            status_info = (
                f"Package {package.id}, Address: {package.address.street_address}, {package.city}, {package.zip}, Weight: {package.mass}, Status: {package.status[1]} at {time_string}, Truck: {package.truck}")
        package.status_change = True if package.status != package.last_status else False
        package.last_status = package.status
        return status_info

    def get_packages(self, file_path: str, address_table: HashTable) -> None:
        from package import Package
        file = open(file_path)
        package_data = csv.reader(file)
        for i, row in enumerate(package_data):
            if i > 7:
                values = row
                #Fun fact: There was a massive bug here because ID was stored as a string instead of an integer.
                deadline = self.get_deadline_from_package(values[5])
                new_package = Package(int(values[0]), address_table.get(values[1]), values[2], values[3], values[4], deadline, values[6],
                                      values[7])
                self.put(new_package.id, new_package)
        for package in self.values():
            if package.co_package:
                self.get_co_packages(package)

    #A function to get the deadline as a Datetime from a string.
    #This function converts the string into a date and then changes the year, month, and day to match the current day.
    def get_deadline_from_package(self, deadline_string:Optional[str]) -> Optional[datetime.datetime]:
        #The function only parses strings that have actual time values.
        if not deadline_string or deadline_string == 'EOD':
            return None
        else:
            current_date = datetime.datetime.now()
            deadline = datetime.datetime.strptime(deadline_string, "%H:%M %p")
            return deadline.replace(year=current_date.year, month=current_date.month, day=current_date.day)

    #A function to change the list of co-package ID's for a package, into a list of actual package objects.
    #This makes it much easier to determine which packages should be delivered together.
    #Big O: O(n) - Only one loop that continues for each n in the co-package list.
    def get_co_packages(self, package) -> None:
        from package import Package
        co_packages = []
        co_packages.append(package)
        for co_package_id in package.co_package:
            co_package = self.get(co_package_id)
            if co_package not in co_packages:
                co_packages.append(co_package)
        package.co_package = co_packages

    def package_lookup_over_time (self, depot):
        from depot import Depot
        packages = self.values()
        #First we need to remove all the status info that was there previously
        for package in packages:
            package.status_change = True
            package.last_status = None
        #Adjust the status by time.
        while config.start_time < config.end_time:
            config.current_time = config.start_time
            for package in packages:
                status_info = (self.package_lookup(package.id))
                if package.status_change:
                    print(status_info)
            #We increase the time by one minute each time
            config.start_time += datetime.timedelta(minutes=1)
        print(f"Total mileage at {config.start_time.strftime('%H:%M %p')} is {depot.get_total_mileage(config.start_time)}")


    def lookup_all(self):
        print(f"Current time is: {config.current_time}")
        packages = self.values()
        for package in packages:
            print(self.package_lookup(package.id))


