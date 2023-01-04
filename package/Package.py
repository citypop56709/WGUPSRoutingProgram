class Package:
    def __init__(self):
        self._id = None
        self._address = None
        self.city = None
        self.state = None
        self.zip = None
        self.deadline = None
        self.mass = None
        self.truck = 0
        self.arrival = None
    @property
    def package_id(self):
        print(f"The {self._id} was accessed.")
        return (self._id)