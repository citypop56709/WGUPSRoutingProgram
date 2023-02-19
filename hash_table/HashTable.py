import datetime
from depot import Depot
from utils import config


# A Hash Table class that implements a chaining hash table that uses linear probing.
# Differs slightly from the implementation in ZyBooks C950 Chapter 7.8 in that you insert key-value pairs as tuples.
class HashTable:
    # HashTable constructor. The hash table is initialized with a for loop that creates a list of array buckets.
    # Each bucket is a list itself. The number of array buckets is 16 by default, but it can be changed as needed.
    # Big O: O(n) - Function has one for loop that initializes the array buckets in the hash table.
    def __init__(self, initial_capacity=16):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # A function that hashes a key and then uses the hash to insert a key-value pair into the appropriate array bucket.
    # The function checks that if the key already exists in the hash table.
    # If it does, then it removes the key-value pair, from the hash table,
    # so that it can be reinserted with the updated value.
    # Big O - O(n) because of the function to get the key and remove it from the list if it exists.
    def insert(self, key, value):
        if self.get(key):
            self.remove(key)
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        bucket_list.append((key, value))

    # A function that retrieves a key-value pair from the hash table given a key.
    # The function hashes the key and then reduces it using the value of the hashed key modulo the length of the table.
    # If the key is not in the table it returns None
    # Big O: O(n) - The function does at least one loop to find the correct key-value pair in the bucket.
    def get(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for (_key, value) in bucket_list:
            if key == _key:
                return value
        else:
            # the key is not found.
            return None

    # A function to remove a key-value pair from the hash table given a key.
    # It uses a for loop to retrieve the correct key-value pair and removes them from the hash table.
    # Big O: O(n) - The function loops through the key-value pairs in the bucket once.
    def remove(self, key) -> None:
        # Get the bucket list where this key-value pair will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # Removes the key-value pair from the bucket if it's present in that bucket.
        for (_key, value) in bucket_list:
            if key == _key:
                bucket_list.remove((key, value))

    # A function that returns a list of every key in the hash table.
    # Big O: O(n^2) - The function has to iterate through the number each array bucket and then each iterate through each key-value pair in the bucket.
    def keys(self):
        res = []
        # Checks every bucket in the hash table.
        for bucket_list in self.table:
            # Adds all the keys to results list.
            for key, value in bucket_list:
                res.append(key)
        #Return all the keys as a list.
        return res

    # A function that returns a list of every value in the hash table.
    # Big O: O(n^2) - The function has to iterate through the number each array bucket and then each iterate through each key-value pair in the bucket.
    def values(self):
        res = []
        # For loop to check every bucket in the hash table.
        for bucket_list in self.table:
            # Adds all the values to the results.
            for key, value in bucket_list:
                res.append(value)
        #Return all the values as a list.
        return res

    # A function to get the current status of a package at a specific time showing where the package is in the delivery.
    # This is the main lookup function for section F in the rubric template.
    # How the function works:
    # The function works by comparing the times of the package attributes to the current time in the program.
    # The times that it compares are for arrival, pickup, en-route, and delivery, in that order.
    # The configuration time represents the current time in the delivery process.
    # If the time is greater than the configuration time then event before that is the current status.
    # The status is saved as a tuple with an integer representing what order the event happens, with a string to describe the event.
    # The status_change attribute is true if the current status is the same as the last status. This represents if they status has changed since the last check.
    # This is so the package has a way to inform the program if a change has happened in its status.
    # Big O: O(1) - The reason why the time complexity is O(1) constant time is because while going through
    # each conditional statement does take time, the time is negligible compared to how long it takes to loop through an array, for an example.
    def status_lookup(self, package_id: int) -> str:
        package = self.get(package_id)
        status_info = None
        if package.pickup_time > config.current_time and package.arrival:
            package.status = (0, "Delayed")
            time_string = datetime.datetime.strftime(package.arrival, "%I:%M %p")
            deadline_string = datetime.datetime.strftime(package.deadline, "%I:%M %p") if package.deadline else "EOD"
            status_info = f"Package {package.id}, Address: {package.address.street_address}, {package.city}, {package.zip}, " \
                          f"Weight: {package.mass}, Status: {package.status[1]} arriving at {time_string}, Deadline: {deadline_string}"
            package.status_change = True if package.status != package.last_status else False
            package.last_status = package.status
            return status_info
        if package.pickup_time > config.current_time and not package.arrival:
            package.status = (1, "At Hub")
            deadline_string = datetime.datetime.strftime(package.deadline, "%I:%M %p") if package.deadline else "EOD"
            status_info = (
                f"Package {package.id}, Address: {package.address.street_address}, {package.city}, {package.zip}, "
                f"Weight: {package.mass}, Status: {package.status[1]}, Deadline: {deadline_string}")
            package.status_change = True if package.status != package.last_status else False
            package.last_status = package.status
            return status_info
        elif package.en_route_time > config.current_time:
            package.status = (2, "Picked Up")
            time_string = datetime.datetime.strftime(package.pickup_time, "%I:%M %p")
            deadline_string = datetime.datetime.strftime(package.deadline, "%I:%M %p") if package.deadline else "EOD"
            status_info = (
                f"Package {package.id}, Address: {package.address.street_address}, {package.city}, {package.zip}, "
                f"Weight: {package.mass}, Status: {package.status[1]} at {time_string}, Deadline: {deadline_string}, Truck: {package.truck}")
        elif package.delivery_time > config.current_time:
            package.status = (3, "En Route")
            time_string = datetime.datetime.strftime(package.en_route_time, "%I:%M %p")
            deadline_string = datetime.datetime.strftime(package.deadline, "%I:%M %p") if package.deadline else "EOD"
            status_info = (
                f"Package {package.id}, Address: {package.address.street_address}, {package.city}, {package.zip}, "
                f"Weight: {package.mass}, Status: {package.status[1]} at {time_string}, Deadline: {deadline_string}, Truck: {package.truck}")
        else:
            package.status = (4, "Delivered")
            time_string = datetime.datetime.strftime(package.delivery_time, "%I:%M %p")
            deadline_string = datetime.datetime.strftime(package.deadline, "%I:%M %p") if package.deadline else "EOD"
            status_info = (
                f"Package {package.id}, Address: {package.address.street_address}, {package.city}, {package.zip}, "
                f"Weight: {package.mass}, Status: {package.status[1]} at {time_string}, Deadline: {deadline_string}, Truck: {package.truck}")
        package.status_change = True if package.status != package.last_status else False
        package.last_status = package.status
        return status_info

    # A function that prints out every package status and then prints out statuses as they change within a time range.
    # This makes it possible for the user to check packages during a time range.
    # The function works by getting a list of packages by using the hash table's values() function.
    # Then it uses a for loop to change each package's status_change and last_status attributes. It does this so that the results of
    # previous operations will not affect the current one.
    # It then uses a while loop that continues while the start time is less than the end time of the given time range.
    # It updates each package's status at that given time, then it adds a minute to the start time.
    # The function only prints the package's status if a change was detected. It uses the status_change attribute to measure changes.
    # At the end it uses the passed-in Depot object to print the total mileage at the finished time.
    # Big O: O(n^2) - Time complexity is O(n^2) because the function has to loop through each minute in the time range and
    # then loop through each package in that time.
    def package_lookup_over_time(self, depot: Depot) -> None:
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
            # We increase the time by one minute each loop.
            config.start_time += datetime.timedelta(minutes=1)
        print(
            f"Total mileage at {config.start_time.strftime('%I:%M %p')} is {depot.get_total_mileage(config.start_time)}")

    # A function to display the package status for every package in the hash table.
    # This works by getting all the packages in the table using the hash table's values function, sorting them by delivery time using a lambda expression,
    # then it prints out the status of each package, then it prints out the total mileage.
    # Big O: O(n log n) - The slowest part of the algorithm is sorting each package by delivery time. The time complexity for Python's built-in Timsort algorithm is O(n log n) worst case.
    def lookup_all(self, depot: Depot) -> None:
        print(f"Current time is: {config.current_time}")
        packages = self.values()
        packages.sort(key=lambda x:x.delivery_time)
        for package in packages:
            print(self.status_lookup(package.id))
        print(
            f"Total mileage at {config.current_time.strftime('%I:%M %p')} is {depot.get_total_mileage(config.current_time)}")
