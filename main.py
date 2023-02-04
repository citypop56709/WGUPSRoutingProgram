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
    config.current_time = datetime.datetime.today()
    depot.trucks[0].deliver_packages()
    depot.trucks[1].deliver_packages()
    print(config.total_mileage)
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
        if option == "3":
            while True:
                try:
                    user_time_string = input("Set the current time using the format HH:MM am/pm: ")
                    user_time = datetime.datetime.strptime(user_time_string, "%H:%M %p")
                    config.current_time = config.current_time.replace(hour=user_time.hour, minute=user_time.minute,
                                                                      second=0)
                    break
                except ValueError:
                    print("Invalid input. Please input time using the correct format.")
            package_list = packages.values()
            for package in package_list:
                package.get_status(config.current_time)
            package_list.sort(key=lambda x:x.status[0])
            for package in package_list:
                print(package.status_info)
        if option == "4":
            quit()

    display_menu_options()



if __name__ == '__main__':
    main()
