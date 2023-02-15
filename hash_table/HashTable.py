import datetime
from utils import config

"""
A Hash Table class that implements a hash table using chaining and linear probing.
Differs slightly from the implementation in 7.8 in that you insert keys and values at the same time.
This makes it easier to pull a value from the given key. If they key is already in the hash table when a value is added the key gets deleted.
This also helps because if a key has the same hash as another key, it will check to see if the keys are actually the same before returning a value.
"""
class HashTable:
    # HashTable constructor. Initial capacity is optional.
    def __init__(self, initial_capacity=16):
        self.table = []
        # The capacity is implemented by adding empty array buckets to the table.
        for i in range(initial_capacity):
            self.table.append([])

    # Inserts a new key, value pair into the hash table.
    def put(self, key, value):
        # If the key is already in the hash table then we want to remove it, and replace its value.
        if self.get(key):
            self.remove(key)
        # get the bucket list where this item will go.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # insert the key, value pair into the bucket list.
        bucket_list.append((key, value))

    # Searches for an value in the hash table using a given key.
    # Overall time complexity is O(n) the reason why is that it has
    # to perform at least one loop to find all the key, value pairs in the given bucket.
    def get(self, key):
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # Search through all the key value pairs and see if the key matches a key in the bucket's pairs.
        for (_key, value) in bucket_list:
            if key == _key:
                return value
        else:
            # the key is not found.
            return None

    # Removes a key, value pair from the hash table given a specific key.
    def remove(self, key):
        # get the bucket list where this key, value pair will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # remove the key, value pair from the bucket if it's present in that bucket
        for (_key, value) in bucket_list:
            if key == _key:
                bucket_list.remove((key, value))

    # A function that returns a list of every key in the hash table.
    # Time Complexity is O(n*m) where n is the number of buckets in the hash table, and m is the number of key, value pairs in the bucket.
    # This is because it has to perfrom two for loops to retrieve all the data.
    def keys(self):
        res = []
        # Check every bucket in hash table
        for bucket_list in self.table:
            # Adds all the keys to results.
            for key, value in bucket_list:
                res.append(key)
        #Return all the keys as a list.
        return res

    #A function that returns a list of every value in the hash table.
    #Time Complexity is O(n*m) where n is the number of buckets in the hash table, and m is the number of key, value pairs in the bucket.
    #This is because it has to perform two loops to retrieve all the data.
    def values(self):
        res = []
        #Check every bucket in the hash table
        for bucket_list in self.table:
            #Adds all the values to the results.
            for key, value in bucket_list:
                res.append(value)
        #Return all the values as a list.
        return res

    # A function to get the current status of a package given a specific time.
    # This tells you where that package was.
    # It works by checking the time compared to each stage of the package and then sets the status to a string.
    # The program uses tuples to make sorting by package status simple.
    def status_lookup(self, id: int):
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
            status_info = (
                f"Package {package.id}, Address: {package.address.street_address}, {package.city}, {package.zip}, Weight: {package.mass}, Status: {package.status[1]}")
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

    def package_lookup_over_time(self, depot):
        from depot import Depot
        packages = self.values()
        # First we need to remove all the status info that was there previously
        for package in packages:
            package.status_change = True
            package.last_status = None
        # Adjust the status by time.
        while config.start_time < config.end_time:
            config.current_time = config.start_time
            for package in packages:
                status_info = (self.status_lookup(package.id))
                if package.status_change:
                    print(status_info)
            # We increase the time by one minute each time
            config.start_time += datetime.timedelta(minutes=1)
        print(
            f"Total mileage at {config.start_time.strftime('%H:%M %p')} is {depot.get_total_mileage(config.start_time)}")

    def lookup_all(self):
        print(f"Current time is: {config.current_time}")
        packages = self.values()
        for package in packages:
            print(self.status_lookup(package.id))

