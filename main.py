from truck.Truck import Truck
from utils import Distances, PackageTable


def main():
    address_list = Distances.get_addresses_from_file(r"Documentation/WGUPS Distance Table.xlsx")
    for address in address_list:
        print(address.distances)
    packages = PackageTable.get_packages(r"Documentation/WGUPS Package File.xlsx")
    truck1 = Truck(address_list, packages)




if __name__ == '__main__':
    main()
