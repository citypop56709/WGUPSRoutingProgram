from utils import config
from depot import Depot
from utils import PackageTable

#A function to generate the user interface.
#Parameters:
# packages -> Takes in a PackageTable that is a specialized HashTable specifically for packages.
# depot -> Takes in a

def display_menu_options(packages: PackageTable, depot: Depot):
    print("1. Print All Package Status and Total Mileage")
    print("2. Get a Single Package Status with a Time")
    print("3. Get All Package Status with a Time")
    print("4. Exit the Program")
    option = input("Select an option: ")
    if option == "1":
        try:
            config.start_time = config.set_time(config.start_time, "start")
            config.end_time = config.set_time(config.end_time, "end")
            packages.package_lookup_over_time(depot)
            input()
        except ValueError:
            print("Invalid input.")
        display_menu_options(packages, depot)
    if option == "2":
        try:
            config.current_time = config.set_time(config.current_time, "current")
            package_id = input("Enter in a valid package ID: ")
            status_info = packages.package_lookup(package_id)
            print(status_info)
            input()
        except ValueError:
            print("Invalid input.")
        except AttributeError:
            print("Invalid package ID. Please select a package from 1-40.")
        display_menu_options(packages, depot)
    if option == "3":
        try:
            config.current_time = config.set_time(config.current_time, "current")
            packages.lookup_all()
            input()
        except ValueError:
            print("Invalid input.")
        display_menu_options(packages, depot)
    if option == "4":
        quit()