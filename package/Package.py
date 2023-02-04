import datetime
from typing import Optional
from utils import config
from address import Address


class Package:
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
        self.status_info = None

    #A function to get the current status of a package given a specific time.
    #This tells you where that package was.
    #It works by checking the time compared to each stage of the package and then sets the status to a string.
    #The program uses tuples to make sorting by package status simple.
    def get_status(self, time:datetime):
        if self.pickup_time > config.current_time and self.arrival:
            self.status = (0, "Delayed")
            time_string = datetime.datetime.strftime(self.arrival, "%H:%M %p")
            self.status_info = f"Package {self.id}, Status: {self.status[1]} arriving at {time_string}"
            return
        if self.pickup_time > config.current_time and not self.arrival:
            self.status = (1, "At Hub")
            time_string = datetime.datetime.strftime(config.current_time, "%H:%M %p")
            self.status_info = (f"Package {self.id}, Status: {self.status[1]} at {time_string}")
            return
        if self.en_route_time > config.current_time:
            self.status = (2, "Picked Up")
            time_string = datetime.datetime.strftime(self.pickup_time, "%H:%M %p")
            self.status_info = (
                f"Package {self.id}, Status: {self.status[1]} at {time_string}, Truck: {self.truck}")
        elif self.delivery_time > config.current_time:
            self.status = (3, "En Route")
            time_string = datetime.datetime.strftime(self.en_route_time, "%H:%M %p")
            self.status_info = (
                f"Package {self.id}, Status: {self.status[1]} at {time_string}, Truck: {self.truck}")
        else:
            self.status = (4, "Delivered")
            time_string = datetime.datetime.strftime(self.delivery_time, "%H:%M %p")
            self.status_info = (
                f"Package {self.id}, Status: {self.status[1]} at {time_string}, Truck: {self.truck}")


    def set_truck2(self, s: str):
        if s and type(s) != float:
            if "can only be on truck 2" in s.lower():
                return True
        else:
            return False

    def set_arrival(self, s: str):
        if s and type(s) != float:
            return self.get_arrival_from_string(s)
        else:
            return None

    """
    Setter function for the co_package attribute. The if statement checks if a package has to be delivered with another one and
    then performs a for loop to remove all the extra characters in the string and only return a list of which packages need to be delivered with it.
    """
    def set_co_package(self, s: str):
        #Extract the package id's from the string
        if s and type(s) != float:
            if "must be delivered with" in s.lower():
                res = ''
                for i in range(len(s)):
                    if not s[i].isalpha():
                        res += s[i]
                #Split the string making the string into a list of all the values.
                split_list = res.split(',')
                #Turn all these strings into integers
                for i in range(len(split_list)):
                    split_list[i] = int(split_list[i])
                return split_list
            else:
                return None
        else:
            return None

    #A function that retrieves the arrival data from a package's notes.
    #It works by creating a new string that strips any spaces or symbols from the note
    #Then it parses the string for the time data
    #It then creates a datetime based on that data, by replacing the hours and minutes of today's time
    #With the time from the package note.
    #Time Complexity: O(n) because the function only uses one for loop to parse the string.
    def get_arrival_from_string(self, s: str):
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
