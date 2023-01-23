import datetime
from typing import Optional
import time
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
        self.status = None
        self.truck2 = self.set_truck2(note)
        self.arrival = self.set_arrival(note)
        self.co_package = self.set_co_package(note)

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
        if s and type(s) != float:
            if "must be delivered with" in s.lower():
                res = ''
                for i in range(len(s)):
                    if not s[i].isalpha():
                        res += s[i]
                return res.split()
            else:
                return None
        else:
            return None

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
            return time.strptime(arrival_time, "%I%M%p") if arrival_time else None
        except ValueError:
            return None


