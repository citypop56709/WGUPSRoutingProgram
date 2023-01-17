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
        for i in range(size):
            self.buckets.append([])

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
        bucket = hash(key) % self.size
        if self.get(key):
            for i in range(len(self.buckets[bucket])):
                if self.buckets[bucket][i][0] == key:
                    self.buckets[bucket][i][1] = value
                    return
            else:
                self.buckets[bucket].append((key, value))
        else:
            self.buckets[bucket].append((key, value))

    """
    A function that gets the key from the hash table and returns the value the key is associated with.
    How it works:
    1. The index is based on hash of the key constrained by the size of the hash table.
    2. If there is a bucket occupied by that index then the function uses linear probing to find
    which value in the bucket matches the key.
    3. If the value is found then return it.
    4. If the key is not in the bucket array then we return None
    """
    def get(self, input_key):
        bucket = hash(input_key) % self.size
        if self.buckets[bucket]:
            values = self.buckets[bucket]
            for key, value in values:
                if input_key == key:
                    return value
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
    A function to return the keys in the hash table as a list. This is useful when you're trying to iterate
    through all the keys at once.
    """
    def keys(self):
        keys_list = []
        for i in range(len(self.buckets)):
            if self.buckets[i]:
                for j in range(len(self.buckets[i])):
                    keys_list.append(self.buckets[i][j][0])
        return keys_list


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
