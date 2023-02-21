import datetime
from typing import Optional
from address import Address

# A class that creates a package object.
# The package object stores all the information for each package in a single object.
# This makes it simple to get the correct package information.
class Package:
    # A constructor for the package class.
    # Each parameter is based on columns in the packages CSV file.
    # The package also contains attributes that track the time the package is picked up from the depot,
    # the time that it begins its delivery, and the time it actually gets delivered.
    # The status_change and last_status attributes are for tracking the package's status over time.
    def __init__(self, id: int, address: Address, city: str, state: str, zip: str, deadline: object, mass: int,
                 note: Optional[str]):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.mass = mass
        self.note = note
        self.truck2 = self.set_truck2(note)
        self.arrival = self.set_arrival(note)
        self.truck = None
        self.pickup_time = None
        self.en_route_time = None
        self.delivery_time = None
        self.co_package = self.set_co_package(note)
        self.status = None
        self.status_change = False
        #This is necessary. Otherwise, there is no way to check if the package's status changed previously.self.last_status = None
        self.last_status = None

    # A function that checks the notes string to see if the package can only be on truck #2.
    def set_truck2(self, s: str):
        if s and type(s) != float:
            if "can only be on truck 2" in s.lower():
                return True
        else:
            return False

    # A function that checks the notes string to see if the package has a delay with a later arrival date.
    # It calls the function get_arrival to retrieve the information from the notes string.
    def set_arrival(self, s: str):
        if s and type(s) != float:
            return self.get_arrival(s)
        else:
            return None

    # A setter function for the co_package attribute.
    # The if statement checks if a package has to be delivered with another one and,
    # then performs a for loop to remove all the extra characters in the string.
    # It then returns an integer list of which package IDs are co-packages.
    # Big O: O(n) - There are multiple for loops that parses through each character in the string, but only one loop is running at a time.
    def set_co_package(self, s: str):
        if s and type(s) != float:
            if "must be delivered with" in s.lower():
                res = ''
                for i in range(len(s)):
                    if not s[i].isalpha():
                        res += s[i]
                #Split the string, converting the string into a list of characters.
                split_list = res.split(',')
                #Converts the strings into integers
                for i in range(len(split_list)):
                    split_list[i] = int(split_list[i])
                return split_list
            else:
                return None
        else:
            return None

    # A function that retrieves the arrival data from a package's notes.
    # It creates a new string that strips any spaces or non-alphanumeric characters from the note string.
    # Then, it parses the string for the time data using if statements.
    # It then creates a datetime object based on that data,
    # by replacing the hours and minutes of the current time with the one from the notes.
    # Big O: O(n) because the function only uses one for loop to parse each character in the string.
    def get_arrival(self, s: str):
        arrival_time = ""
        new_string = "".join([i for i in s.lower() if i.isalnum()])
        for i in range(len(new_string)):
            if new_string[i].isdigit():
                arrival_time += new_string[i]
            elif new_string[i] == ":":
                arrival_time += new_string[i]
            elif (
                    arrival_time
                    and new_string[i: i + 2] == "am"
                    or new_string[i: i + 2] == "pm"
            ):
                arrival_time += new_string[i: i + 2]
            else:
                pass
        try:
            arrival_hours_minutes =  datetime.datetime.strptime(arrival_time, "%I%M%p") if arrival_time else None
            return datetime.datetime.now().replace(hour=arrival_hours_minutes.hour, minute=arrival_hours_minutes.minute)
        except ValueError:
            return None
        except AttributeError:
            return None
