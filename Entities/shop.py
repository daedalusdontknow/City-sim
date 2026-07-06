import math
import random
import uuid

from Entities.buildings import Building
from Managers.logger import Logger
from config import Preview, EconomyValues


class Shop:
    shops = {}

    def __init__(self, shop_id, x, y, x2, y2, capacity):
        self.shop_id = str(shop_id)
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2
        self.capacity = capacity

    @staticmethod
    def create_shop(x, y, x2, y2, capacity):
        uid = str(uuid.uuid4())
        new_shop = Shop(uid, x, y, x2, y2, capacity)
        Shop.shops[uid] = new_shop
        Building.add_building(x, y, x2, y2)
        return new_shop

    @staticmethod
    def get_by_id(target_uuid):
        return Shop.shops.get(str(target_uuid))

    @staticmethod
    def get_nearest_shop(x, y):
        nearest = None
        distance = float('inf')

        for shop in Shop.shops.values():
            dx = x - shop.x
            dy = y - shop.y
            dist_sq = dx**2 + dy**2

            if dist_sq < distance:
                nearest = shop
                distance = dist_sq

        return nearest

    @staticmethod
    def spawn_shops(count):
        for _ in range(count):
            shop_area = 400
            final_x, final_y, final_x2, final_y2 = 0, 0, 0, 0

            max_attempts = 10
            attempts = 0
            valid_position = False

            while not valid_position and attempts < max_attempts:
                base_side = math.sqrt(shop_area)
                aspect_ratio = random.uniform(0.8, 1.2)
                width = base_side * aspect_ratio
                height = shop_area / width
                w = max(2, int(width))
                h = max(2, int(height))

                x = random.randint(0, Preview.picture_width - w)
                y = random.randint(0, Preview.picture_height - h)
                x2 = x + w
                y2 = y + h

                if not Building.check_if_collides(x, y, x2, y2):
                    valid_position = True
                    final_x, final_y, final_x2, final_y2 = x, y, x2, y2
                else:
                    attempts += 1

            if valid_position:
                actual_area = (final_x2 - final_x) * (final_y2 - final_y)
                capacity = int(actual_area / EconomyValues.shop_area_per_customer)
                Shop.create_shop(final_x, final_y, final_x2, final_y2, capacity)
            else:
                Logger.log("[Error]", "kunne ikke finde plads til shop")

    @staticmethod
    def check_and_expand(total_population):
        total_capacity = sum(s.capacity for s in Shop.shops.values())
        if total_capacity < total_population:
            Shop.spawn_shops(1)
            Logger.log("[Shop]", "En ny shop er blevet bygget for at imødekomme befolkningens behov.")