from package import Package

class Truck:
    def __init__(self, id, package_list: list[Package]):
        self.id = id
        self.current = None # Current address
        self.speed = float(18)

