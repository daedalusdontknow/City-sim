import math
import random
import uuid

from Entities.buildings import Building
from Managers.logger import Logger
from config import Preview


class House:

    houses = {}

    def __init__(self, house_id, x, y, x2, y2, capacity):
        self.house_id = str(house_id)
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2
        self.capacity = capacity

    @staticmethod
    def create_house(x, y, x2, y2, capacity):
        uid = str(uuid.uuid4())
        new_house = House(uid, x, y, x2, y2, capacity)
        House.houses[uid] = new_house
        Building.add_building(x, y, x2, y2)
        return new_house

    @staticmethod
    def get_by_id(target_uuid):
        return House.houses.get(str(target_uuid))

    @staticmethod
    def spawn_houses(count, humans):
        houses = []

        capacity = math.ceil(humans / count)
        area = capacity * 12

        for _ in range(count):
            base_side = math.sqrt(area)
            aspect_ratio = random.uniform(0.8, 1.2)

            width = base_side * aspect_ratio
            height = area / width
            final_x, final_y, final_x2, final_y2 = 0, 0, 0, 0

            max_attempts = 10
            attempts = 0
            valid_position = False

            while not valid_position and attempts < max_attempts:
                base_side = math.sqrt(area)
                aspect_ratio = random.uniform(0.8, 1.2)

                width = base_side * aspect_ratio
                height = area / width

                w = max(2, int(width))
                h = max(2, int(height))

                x = random.randint(0, Preview.picture_width - w)
                y = random.randint(0, Preview.picture_height - h)

                x2 = x + w
                y2 = y + h

                if not Building.check_if_collides(x, y, x2, y2):
                    valid_position = True
                    final_x, final_y, final_x2, final_y2 = x, y, x2, y2

                attempts += 1

            if valid_position:
                houses.append(House.create_house(final_x, final_y, final_x2, final_y2, capacity))

        return houses

    @staticmethod
    def cleanup_empty_houses(all_humans):
        occupied_uuids = {h.stats.get("house_uuid") for h in all_humans if h.stats.get("house_uuid")}
        empty_houses = [h_id for h_id in House.houses if h_id not in occupied_uuids]

        for h_id in empty_houses:
            house = House.houses[h_id]
            Building.remove_building(house.x, house.y, house.x2, house.y2)
            Logger.log("[House]", f"Hus {h_id} blev fjernet, da det var tomt.")
            del House.houses[h_id]