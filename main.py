from depot import Depot
from utils import Distances, PackageTable, config
from utils import Interface


#Ayun Daywhea
#adaywhe@wgu.edu
#12 Feb 2023
#ID: 001177960
#Main function for the WGUPSRouting Program
#This function does four things:
#1.Gets the file paths for the csv file .
#2.Creates the depot object and loads the values from the csv into it.
#3.Runs the package delivery algorithm.
#4.Runs the menu interface so that the users have some way of interfacing with the function.
#Everything else is contained in separate packages and classes.
#The point of this was to organize code in way that incentivized code re-use.
def main():
    distance_file_path = r"Documentation/WGUPS Distance Table.csv"
    package_file_path = r"Documentation/WGUPS Package File.csv"
    address_list = Distances.get_addresses_from_file(distance_file_path)
    address_table = Distances.get_address_table(address_list)
    packages = PackageTable()
    packages.get_packages(package_file_path, address_table)
    depot = Depot(address_list, packages)
    depot.load_trucks()
    #The program delivers all the packages first, and then tracks where each package is in the delivery process,
    #So when a user checks backwards or forwards in time the information is correct.
    depot.trucks[0].deliver_packages()
    depot.trucks[1].deliver_packages()
    Interface.display_menu_options(packages, depot)



if __name__ == '__main__':
    main()
