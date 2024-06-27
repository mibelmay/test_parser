class Advertisement:

    def __init__(self, url, cost,
                 rooms_count,
                 type_of_deal,
                 type_of_building,
                 street,
                 house,
                 floor,
                 square):
        self.url = url
        self.cost = cost
        self.rooms_count = rooms_count
        self.type_of_deal = type_of_deal
        self.type_of_building = type_of_building
        self.street = street
        self.house = house
        self.floor = floor
        self.square = square

    def __str__(self):
        return f'Cost: {self.cost}, Rooms: {self.rooms_count}, Square: {self.square}, Url: {self.url}'
