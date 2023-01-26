import datetime
from typing import Optional
from hash_table import HashTable
from package import Package
import csv

class PackageTable:

    @classmethod
    def get_packages(cls, file_path: str, address_table: HashTable):
        package_table = HashTable()
        file = open(file_path)
        package_data = csv.reader(file)
        for i, row in enumerate(package_data):
            if i > 7:
                values = row
                #Fun fact: There was a massive bug here because ID was stored as a string instead of an int.
                deadline = PackageTable.get_deadline_from_package(values[5])
                new_package = Package(int(values[0]), address_table.get(values[1]), values[2], values[3], values[4], deadline, values[6],
                                      values[7])
                package_table.put(new_package.id, new_package)
        return package_table

    #A function to get the deadline as a Datetime from a string.
    #This function converts the string into a date and then changes the year, month, and day to match the current day.
    @classmethod
    def get_deadline_from_package(cls, deadline_string:Optional[str]) -> Optional[datetime.datetime]:
        #The function only parses strings that have actual time values.
        if not deadline_string or deadline_string == 'EOD':
            return None
        else:
            current_date = datetime.datetime.now()
            deadline = datetime.datetime.strptime(deadline_string, "%H:%M %p")
            return deadline.replace(year=current_date.year, month=current_date.month, day=current_date.day)



