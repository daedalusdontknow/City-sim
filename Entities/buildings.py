import uuid

class Building:

    buildings = {}

    def __init__(self, x, y, x2, y2):
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2

    @staticmethod
    def add_building(x, y, x2, y2):
        uid = str(uuid.uuid4())
        new_building = Building(x, y, x2, y2)
        Building.buildings[uid] = new_building
        return new_building

    @classmethod
    def remove_building(cls, x, y, x2, y2):
        building_rect = (x, y, x2, y2)
        if building_rect in cls.buildings:
            cls.buildings.remove(building_rect)

    @staticmethod
    def check_if_collides(x, y, x2, y2):
        for building in Building.buildings.values():
            if (x < building.x2 and x2 > building.x and
                    y < building.y2 and y2 > building.y):
                return True
        return False