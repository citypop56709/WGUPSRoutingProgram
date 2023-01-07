import datetime
from typing import Optional


class Package:
    def __init__(self, id:int, address:str, city:str, state:str, zip:str, deadline:object, mass:int, note:Optional[str]):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.mass = mass
        self.arrival = None
        self.note = note
        self.truck2 = False

    """    
    Reads the memo and set's the truck2 flag to True if it requires Truck 2 for deliveries.
    """
    def is_truck2(self, note:str):
        if "can only be on truck 2" in note.lower(): self.truck2 = True

    """
    Reads the memo and set's the arrival time from none to a special arrival time frame.
    """
    def find_arrival(self, note:str):
        time = ''
        new_string = ''.join([i for i in note.lower() if i.isalnum()])
        for i in range(len(new_string)):
            if new_string[i].isdigit():
                time += new_string[i]
            elif new_string[i] == ':':
                time += new_string[i]
            elif time and new_string[i:i+2] == 'am' or new_string[i:i+2] == 'pm':
                time += new_string[i:i+2]
            else:
                pass
        return time






