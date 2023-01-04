from typing import Optional


# hash_table class using chaining.
class HashTable:
    def __init__(self, size=16):
        self.buckets = []
        self.size = 16
        self.bucket_count = 0
        self.__expand_buckets(self.size)

    """
    How this works: This function expands the size of the hash table in a logical manner. 
    """

    def __expand_buckets(self, new_size, start=0) -> None:
        for i in range(start, new_size):
            self.buckets.append([])
        if self.size != new_size:
            self.size = new_size

    """
    How this works: This function first checks the size of the buckets to see if we need to expand the hash table or not.
    """

    def put(self, key, value):
        # Checks if the hash table needs to be expanded or not.
        if self.bucket_count >= (self.size // 2):
            self.__expand_buckets(self.size, (self.size * 2))

        index = hash(key) % self.size
        if self.get(key):
            # update the bucket if it exists already
            # stops at the first match and returns
            for i in range(len(self.buckets[index])):
                if self.buckets[index][i][0] == key:
                    self.buckets[index][i][1] = value
                    return
        else:
            self.buckets[index].append((key, value))

    # Method to retrieve the values from the hash table
    def get(self, key) -> Optional["object"]:
        index = hash(key) % self.size
        if self.buckets[index]:
            # find the item's index and return the item that is in the bucket list.
            # this process uses linear probing to find the key
            values = self.buckets[index]
            for i in range(len(values)):
                if self.buckets[index][i][0] == key:
                    return self.buckets[index][i][1]
        else:
            # the key is not found.
            return None

    # Removes an item with matching key from the hash table.
    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % self.size
        bucket_list = self.buckets[bucket]

        # remove the item from the bucket list if it is present.
        if key in bucket_list:
            bucket_list.remove(key)

    #Displays a list of keys in the Hash Table.
    def keys(self):
        key_list = []
        for i in range(len(self.buckets)):
            if self.buckets[i]:
                for j in range(len(self.buckets[i])):
                    key_list.append(self.buckets[i][j][0])
        return key_list

    #Displays a list of values in the Hash Table.
    def values(self):
        values_list = []
        for i in range(len(self.buckets)):
            if self.buckets[i]:
                for j in range(len(self.buckets[i])):
                    values_list.append(self.buckets[i][j][1])
        return values_list

    #Returns the Hash Table as a string in the format {key, value}.
    def __repr__(self):
        return_val = "{"
        key_value_zip = list(zip(self.keys(), self.values()))
        add_comma = True
        for key, value in key_value_zip:
            add_comma = not add_comma
            if add_comma:
                return_val += ', '
            return_val += "%s:%s" % (key, value)
        return return_val + '}'
