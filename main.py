from utils import AddressTable, Distances, PackageList


def main():
    distance_file_path = r"Documentation/WGUPS Distance Table.xlsx"
    address_file_path = r"Documentation/WGUPS Distance Table.xlsx"
    package_file_path = r"Documentation/WGUPS Package File.xlsx"
    distances = Distances(distance_file_path)
    address_table = AddressTable.get_addresses(address_file_path, len(distances.graph))
    packages = PackageList.get_packages(package_file_path, address_table)
    print(distances.get_min_distance(packages[:3], address_table))


if __name__ == '__main__':
    main()
