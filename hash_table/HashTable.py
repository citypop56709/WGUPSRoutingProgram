from typing import Optional


# hash_table class using chaining.
class HashTable:

    """
    A constructor for the hash table. The hash table stores key value pairs using buckets.
    The hash table is initialized to a size of 16 and has a size attribute to easily keep track
    of how many buckets are in the hash table. The bucket count attribute tracks how many buckets
    are actively used.
    """
    def __init__(self, size=16):
        self.buckets = []
        self.size = 16
        self.bucket_count = 0
        self.__expand_buckets(self.size)

    """
    A function that expands the hash table and updates the size if the buckets reach a certain capacity.
    How this works: 
    1. The size that's passed in is based on the put function. It's always twice the size of the original hash table.
    2. The function appends empty buckets in the range of the new size.
    3. If this is called at the start then the size value stays at 16. Otherwise we update it.
    """

    def __expand_buckets(self, new_size, start=0) -> None:
        for i in range(start, new_size):
            self.buckets.append([])
        if self.size != new_size:
            self.size = new_size

    """
    A function to put a key and value into the hash table.
    How this works: 
    1. This function first checks the size of the buckets to see if we need to expand
    the hash table or not. If we do it expands it according to the __expand_buckets method.
    2. The index is based on hash of the key constrained withe size of the hash table.
    3. We check if the key exists in the hash table using the get function. If it does then we update the value.
    If there is a collision because the hash is the same as another key then we perform chaining by appending
    the tuple to the same bucket.
    4. If the key is not in the hash table then we append the tuple to the appropriate bucket.
    """
    def put(self, key, value):
        if self.bucket_count >= (self.size // 2):
            self.__expand_buckets(self.size, (self.size * 2))

        index = hash(key) % self.size
        if self.get(key):
            for i in range(len(self.buckets[index])):
                if self.buckets[index][i][0] == key:
                    self.buckets[index][i][1] = value
                    return
            else:
                self.buckets[index].append((key, value))
        else:
            self.buckets[index].append((key, value))
        self.bucket_count += 1

    """
    A function that gets the key from the hash table and returns the value the key is associated with.
    How it works:
    1. The index is based on hash of the key constrained by the size of the hash table.
    2. If there is a bucket occupied by that index then the function uses linear probing to find
    which value in the bucket matches the key.
    3. If the value is found then return it.
    4. If the key is not in the bucket array then we return None
    """
    def get(self, key):
        index = hash(key) % self.size
        if self.buckets[index]:
            values = self.buckets[index]
            for i in range(len(values)):
                if self.buckets[index][i][0] == key:
                    return self.buckets[index][i][1]
        else:
            return None

    """
    A function to remove a key from the hash table. This is done in two ways:
    1. Get the bucket that the value should be located in based on the key's hash.
    2. If the key is in the bucket that it should be in then remove it.
    """
    def remove(self, key):
        bucket = hash(key) % self.size
        bucket_list = self.buckets[bucket]

        if key in bucket_list:
            bucket_list.remove(key)

    """
    A function return the values in the keys of the hash table as a list. Useful for iterating over all the keys at once.
    """
    def keys(self):
        key_list = []
        for i in range(len(self.buckets)):
            if self.buckets[i]:
                for j in range(len(self.buckets[i])):
                    key_list.append(self.buckets[i][j][0])
        return key_list

    """
    A function to return the values in the hash table as a list. This is useful when you're trying to iterate
    through all the values at once.
    """
    def values(self):
        values_list = []
        for i in range(len(self.buckets)):
            if self.buckets[i]:
                for j in range(len(self.buckets[i])):
                    values_list.append(self.buckets[i][j][1])
        return values_list
