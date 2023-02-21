from depot import Depot
from hash_table import HashTable
from utils import PackageTools
from utils import Interface


# Ayun Daywhea
# adaywhe@wgu.edu
# 21 Feb 2023
# ID: 001177960
# Main function for the WGUPSRouting Program
# This function does four things:
# 1.Gets the file paths for the CSV file.
# 2.Creates an address list and a package hash table based on the CSV files.
# 3.Creates the depot object and loads data from the address list and packages.
# 4.Runs the package delivery algorithm.
# 5.Runs the menu interface so that the users can interface with the function.
# Everything else is contained in separate packages and classes.
# The point of this was to organize code to incentivize code reuse.
def main():
    distance_file_path = r"Documentation/WGUPS Distance Table.csv"
    package_file_path = r"Documentation/WGUPS Package File.csv"
    address_list = PackageTools.get_address_list_from_file(distance_file_path)
    address_table = HashTable()
    PackageTools.set_address_table(address_table, address_list)
    packages = HashTable()
    PackageTools.update_packages_from_csv(package_file_path, packages, address_table)
    depot = Depot(address_list, packages)
    depot.load_trucks()
    # The program delivers all the packages first and then tracks where each package is in the delivery process,
    # So when a user checks backward or forwards in time; the information is correct.
    depot.trucks[0].deliver_packages()
    depot.trucks[1].deliver_packages()
    Interface.display_menu_options(packages, depot)



if __name__ == '__main__':
    main()
