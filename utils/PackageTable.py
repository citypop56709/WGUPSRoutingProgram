import datetime
from typing import Optional
from hash_table import HashTable
import csv

class PackageTable(HashTable):

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


