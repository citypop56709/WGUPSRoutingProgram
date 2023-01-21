from package import Package
from truck import Truck
from truck import Depot
from utils import Distances, PackageTable


def main():
    distance_file_path = r"Documentation/WGUPS Distance Table.csv"
    package_file_path = r"Documentation/WGUPS Package File.csv"
    address_list = Distances.get_addresses_from_file(distance_file_path)
    packages = PackageTable.get_packages(package_file_path)
    print(packages.values())
    #hub_depot = Depot(address_list, packages)











if __name__ == '__main__':
    main()
