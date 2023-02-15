import csv
import datetime
from typing import Optional
from address import Address
from hash_table import HashTable
from package import Package

class PackageTools:

    @classmethod
    def update_packages_from_csv(cls, packages: HashTable, file_path: str, address_table) -> None:
        file = open(file_path)
        package_data = csv.reader(file)
        for i, row in enumerate(package_data):
            if i > 7:
                values = row
                # Fun fact: There was a massive bug here because ID was stored as a string instead of an integer.
                deadline = PackageTools.get_deadline_from_package(values[5])
                new_package = Package(int(values[0]), address_table.get(values[1]), values[2], values[3], values[4],
                                      deadline, values[6],
                                      values[7])
                packages.put(new_package.id, new_package)
        for package in packages.values():
            if package.co_package:
                PackageTools.get_co_packages(packages, package)

    # A function to get the deadline as a Datetime from a string.
    # This function converts the string into a date and then changes the year, month, and day to match the current day.
    @classmethod
    def get_deadline_from_package(cls, deadline_string: Optional[str]) -> Optional[datetime.datetime]:
        # The function only parses strings that have actual time values.
        if not deadline_string or deadline_string == 'EOD':
            return None
        else:
            current_date = datetime.datetime.now()
            deadline = datetime.datetime.strptime(deadline_string, "%H:%M %p")
            return deadline.replace(year=current_date.year, month=current_date.month, day=current_date.day)

    # A function to change the list of co-package ID's for a package, into a list of actual package objects.
    # This makes it much easier to determine which packages should be delivered together.
    # Big O: O(n) - Only one loop that continues for each n in the co-package list.
    @classmethod
    def get_co_packages(cls, packages: HashTable, package: Package) -> None:
        co_packages = []
        co_packages.append(package)
        for co_package_id in package.co_package:
            co_package = packages.get(co_package_id)
            if co_package not in co_packages:
                co_packages.append(co_package)
        package.co_package = co_packages

    """
    Creates a graph that stores in distances a tuple for each address. Each address has an ID based on where it is in Excel.
    When retrieving the distance we can find out the distance to and from by checking if the destination is before or after the start
    as far as ID. This enables us to retrieve a distance to a location and back from a location relatively easily.
    """
    @classmethod
    def get_addresses_from_file(cls, file_path: str):
        address_list = []
        address_id = 0
        try:
            file = open(file_path)
            distance_data = csv.reader(file)
            for i, row in enumerate(distance_data):
                if i > 7:
                    raw_address = row[1]
                    formatted_address = raw_address.split("(")[0].strip()
                    #The distances come as strings, so we have to convert them.
                    distances = [float(x) for x in row[2:] if x]
                    address_list.append(Address(address_id, formatted_address, distances))
                    address_id += 1
            #After the distances are created we then replace the missing values with the correct ones.
            PackageTools.set_null_distances(address_list)
            return address_list
        except FileNotFoundError:
            raise FileNotFoundError("There is no CSV file for the distances.") from None
        except ValueError:
            raise ValueError("The distances are not in a valid format.") from None

    @classmethod
    def update_address_table(cls, address_table, address_list: list[Address]) -> HashTable:
        for address in address_list:
            address_table.put(address.street_address, address)

    @classmethod
    def set_null_distances(cls, address_list:list[Address]) -> None:
        for i in range(len(address_list)):
            for j in range(len(address_list)):
                try:
                    address_list[i].distances[j]
                except IndexError:
                    address_list[i].distances.append(address_list[j].distances[i])