import csv
import datetime
from typing import Optional
from address import Address
from hash_table import HashTable
from package import Package

# A class that contains class methods to make loading data from the CSV files easier.
class PackageTools:

    # A function to load every package from the CSV file into the packages hash table.
    # The function takes in the file path where the CSV is located, a hash table of packages, and a hash table of addresses.
    # It creates package objects using data from the CSV file. After the package object is created it gets inserted into the hash table
    # as a value with the package ID as a key.
    # Big O: O(n log n) - Time complexity is O(n log n) even though there are two separate for loops that have a time complexity of O(n)
    # each, the operation that takes the most time is retrieving the values from the packages hash table using the values() function.    @classmethod
    def update_packages_from_csv(cls, file_path: str, packages: HashTable, address_table: HashTable) -> None:
        file = open(file_path)
        package_data = csv.reader(file)
        for i, row in enumerate(package_data):
            if i > 7:
                values = row
                # Fun fact: There was a massive bug here because the ID was passed into the package constructor
                # as a string instead of as an integer.
                deadline = PackageTools.get_deadline_from_package(values[5])
                new_package = Package(int(values[0]), address_table.get(values[1]), values[2], values[3], values[4],
                                      deadline, values[6], values[7])
                packages.insert(new_package.id, new_package)
        for package in packages.values():
            if package.co_package:
                PackageTools.get_co_packages(packages, package)

    # A function to extract package's delivery deadline time from a string and convert it to a Datetime object.
    @classmethod
    def get_deadline_from_package(cls, deadline_string: Optional[str]) -> Optional[datetime.datetime]:
        # The function ignores cells that have the value EOD because they do not have a deadline.
        if not deadline_string or deadline_string == 'EOD':
            return None
        else:
            current_date = datetime.datetime.now()
            deadline = datetime.datetime.strptime(deadline_string, "%I:%M %p")
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


    # A function that retrieves address data from a CSV file and creates a list of address objects using the data.
    # Big O: O(n^2) - This is because the function has to call the set_null_distances function to adjust the distances for each address.
    @classmethod
    def get_address_list_from_file(cls, file_path: str) -> list[Address]:
        address_list = []
        address_id = 0
        try:
            file = open(file_path)
            distance_data = csv.reader(file)
            for i, row in enumerate(distance_data):
                if i > 7:
                    raw_address = row[1]
                    formatted_address = raw_address.split("(")[0].strip()
                    #The distances are initially formatted as strings, so they have to be converted to floats to be useful.
                    distances = [float(x) for x in row[2:] if x]
                    address_list.append(Address(address_id, formatted_address, distances))
                    address_id += 1
            #After the distances are created we then replace the missing data with the appropriate values using the set_null_distances function.
            PackageTools.set_null_distances(address_list)
            return address_list
        except FileNotFoundError:
            raise FileNotFoundError("There is no CSV file for the distances.") from None
        except ValueError:
            raise ValueError("The distances are not in a valid format.") from None

    # A function to update the values of an empty address hash table using the values from the address list.
    # The function takes in the address_table and the address list as arguments, and uses both to update the
    # hash table using the street address, e.g. 123 Springfield ave, as a key, and an address object as a value.
    # Big O: O(n^2) -> Time complexity is O(n^2) because the insert() function has to be called for each address in the address list.
    @classmethod
    def set_address_table(cls, address_table, address_list: list[Address]) -> None:
        for address in address_list:
            address_table.insert(address.street_address, address)

    # A function that adjust null distances in the distances list for each address with the appropriate distance.
    # The CSV distances files only list distances one-way e.g, if there are two addresses A and B,
    # there will be a distance from distance A to B, but nothing for B to A.
    # This function fills in that gap to make it possible from every single address to find out how far way each other address is.
    # Big O: O(n^2) - This is because the function has two for loops; it has to iterate through each possible address twice.
    @classmethod
    def set_null_distances(cls, address_list:list[Address]) -> None:
        for i in range(len(address_list)):
            for j in range(len(address_list)):
                try:
                    address_list[i].distances[j]
                except IndexError:
                    address_list[i].distances.append(address_list[j].distances[i])