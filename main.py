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
    depot.trucks[0].deliver_packages()
    depot.trucks[1].deliver_packages()
    #User Interface
    def display_menu_options():
        print("1. Print All Package Status and Total Mileage")
        print("2. Get a Single Package Status with a Time")
        print("3. Get All Package Status with a Time")
        print("4. Exit the Program")
        option = input("Select an option: ")
        if option == "1":
            try:
                config.start_time = config.set_time(config.start_time, "start")
                config.end_time = config.set_time(config.end_time, "end")
                packages.get_package_statuses_over_time(config.start_time, config.end_time, depot)
                input()
            except ValueError:
                print("Invalid input.")
            display_menu_options()
        if option == "2":
            try:
                config.current_time = config.set_time(config.current_time, "current")
                package_id = input("Enter in a valid package ID: ")
                package = packages.get(int(package_id))
                package.get_status(config.current_time)
                print(package.status_info)
                input()
            except ValueError:
                print("Invalid input.")
            except AttributeError:
                print("Invalid package ID. Please select a package from 1-40.")
            display_menu_options()
        if option == "3":
            try:
                config.current_time = config.set_time(config.current_time, "current")
                packages.get_package_statuses(config.current_time)
                input()
            except ValueError:
                print("Invalid input.")
            display_menu_options()
        if option == "4":
            quit()
    display_menu_options()



if __name__ == '__main__':
    main()
