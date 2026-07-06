import math
import random
import uuid

from Entities.buildings import Building
from Managers.logger import Logger
from config import Preview, EconomyValues


class Office:
    offices = {}

    def __init__(self, office_id, x, y, x2, y2, capacity):
        self.office_id = str(office_id)
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2
        self.capacity = capacity

    @staticmethod
    def create_office(x, y, x2, y2, capacity):
        uid = str(uuid.uuid4())
        new_office = Office(uid, x, y, x2, y2, capacity)
        Office.offices[uid] = new_office
        Building.add_building(x, y, x2, y2)
        return new_office

    @staticmethod
    def get_by_id(target_uuid):
        return Office.offices.get(str(target_uuid))

    @staticmethod
    def spawn_offices(count, capacity):
        offices = []
        area = capacity * 16

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
                aspect_ratio = random.uniform(0.9, 1.1)
                width = base_side * aspect_ratio
                height = area / width
                w = max(2, int(width))
                h = max(2, int(height))

                final_x = random.randint(0, Preview.picture_width - w)
                final_y = random.randint(0, Preview.picture_height - h)
                final_x2 = final_x + w
                final_y2 = final_y + h

                if not Building.check_if_collides(final_x, final_y, final_x2, final_y2):
                    valid_position = True
                else:
                    attempts += 1

            if valid_position:
                office = Office.create_office(final_x, final_y, final_x2, final_y2, capacity)
                offices.append(office)

        return offices

    @staticmethod
    def get_nearest_office(x, y):
        nearest = None
        distance = float('inf')

        for office in Office.offices.values():
            dx = x - office.x
            dy = y - office.y
            dist_sq = dx ** 2 + dy ** 2

            if dist_sq < distance:
                nearest = office
                distance = dist_sq

        return nearest

    @staticmethod
    def check_and_expand(total_adults):
        total_capacity = sum(o.capacity for o in Office.offices.values())
        if total_capacity < total_adults:
            Office.spawn_offices(1, EconomyValues.new_office_capacity)
            Logger.log("[Office]", f"Kontor oprettet med kapacitet for {EconomyValues.new_office_capacity} ansatte.")