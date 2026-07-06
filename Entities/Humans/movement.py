# Entities/Humans/movement.py
import math
import random
from Entities.house import House
from Entities.office import Office
from Entities.shop import Shop
from config import Preview
from Managers.pathfinder import Pathfinder

def get_path_or_direct(human, b_x, b_y, b_x2, b_y2, target_x, target_y):
    if (b_x - 20 <= human.x <= b_x2 + 20) and (b_y - 20 <= human.y <= b_y2 + 20):
        return []
    return Pathfinder.find_path(human.x, human.y, target_x, target_y)

def move_human(human):
    speed = human.stats["step_length"]

    if "path" not in human.stats:
        human.stats["path"] = []

    target_x, target_y = None, None

    if "goto_work" in human.tasks:
        work = Office.get_by_id(human.tasks["goto_work"])
        if work:
            target_x, target_y = (work.x + work.x2) / 2, (work.y + work.y2) / 2
            if human.status in ["searching_work", "idle"]:
                human.stats["path"] = get_path_or_direct(human, work.x, work.y, work.x2, work.y2, target_x, target_y)
                human.status = "going_to_work"
        else:
            del human.tasks["goto_work"]
            human.status = "idle"

    elif "goto_shop" in human.tasks:
        shop = Shop.get_by_id(human.tasks["goto_shop"])
        if shop:
            target_x, target_y = (shop.x + shop.x2) / 2, (shop.y + shop.y2) / 2
            if human.status in ["searching_food", "idle"]:
                human.stats["path"] = get_path_or_direct(human, shop.x, shop.y, shop.x2, shop.y2, target_x, target_y)
                human.status = "going_to_shop"
        else:
            del human.tasks["goto_shop"]
            human.status = "idle"

    elif "goto_home" in human.tasks:
        house = House.houses.get(human.stats["house_uuid"])
        if house:
            target_x, target_y = (house.x + house.x2) / 2, (house.y + house.y2) / 2
            if human.status in ["walking", "idle"]:
                human.stats["path"] = get_path_or_direct(human, house.x, house.y, house.x2, house.y2, target_x,
                                                         target_y)
                human.status = "going_home"
        else:
            del human.tasks["goto_home"]
            human.status = "idle"

    if human.status in ["going_to_work", "going_to_shop", "going_home"] and target_x is not None:
        if human.stats["path"]:
            target = human.stats["path"][0]
            if move_towards(human, target[0], target[1], speed):
                human.stats["path"].pop(0)

        if not human.stats["path"]:
            if move_towards(human, target_x, target_y, speed):
                if "goto_work" in human.tasks:
                    human.status = "working"
                elif "goto_shop" in human.tasks:
                    human.status = "eating"
                elif "goto_home" in human.tasks:
                    human.status = "sleeping"

    elif human.status not in ["sleeping", "eating", "working"]:
        move_x = random.uniform(-speed, speed)
        move_y = random.uniform(-speed, speed)
        human.x = max(0, min(human.x + move_x, Preview.picture_width))
        human.y = max(0, min(human.y + move_y, Preview.picture_height))

def move_towards(human, tx, ty, speed):
    dx = tx - human.x
    dy = ty - human.y
    distance = math.sqrt(dx ** 2 + dy ** 2)

    if distance <= speed:
        human.x = tx
        human.y = ty
        return True

    angle = math.atan2(dy, dx)
    human.x += math.cos(angle) * speed
    human.y += math.sin(angle) * speed
    return False