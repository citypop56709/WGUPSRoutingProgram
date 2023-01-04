from hash_table import HashTable
from package import Package


def main():
    hash_table = HashTable()
    hash_table.put("A", 10)
    hash_table.put("B", 2)
    print(hash_table)
    print(hash_table.keys())
    print(hash_table.values())


if __name__ == '__main__':
    main()
