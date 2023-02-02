import datetime

from depot import Depot
from utils import Distances, PackageTable, config


def main():
    distance_file_path = r"Documentation/WGUPS Distance Table.csv"
    package_file_path = r"Documentation/WGUPS Package File.csv"
    address_list = Distances.get_addresses_from_file(distance_file_path)
    address_table = Distances.get_address_table(address_list)
    packages = PackageTable()
    packages.get_packages(package_file_path, address_table)
    depot = Depot(address_list, packages)
    depot.load_trucks()
    config.current_time = datetime.datetime.today().replace(hour=13, minute=30, second=0)
    depot.trucks[0].deliver_packages()
    #hub_depot = Depot(address_list, packages)

    #User Interface
    def display_menu_options():
        print("1. Print All Package Status and Total Mileage")
        print("2. Get a Single Package Status with a Time")
        print("3. Get All Package Status with a Time")
        print("4. Exit the Program")
        option = input("Select an option: ")
        if option == "2":
            print("Enter in a valid package ID: ")
            package_id = input()
            try:
                package = packages.get(int(package_id))
                print(package.delivery_info)
                if not package:
                    raise ValueError from None
            except ValueError:
                print("Invalid input.")
            print()
        if option == "4":
            quit()
    #display_menu_options()



if __name__ == '__main__':
    main()
