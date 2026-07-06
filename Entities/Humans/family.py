import random
import math

from Managers.logger import Logger
from config import FamilyValues, Preview
from Entities.house import House
from Entities.buildings import Building
from Entities.Humans.spawner import create_human_instance

def get_human_by_id(humans_list, h_id):
    for h in humans_list:
        if h.h_id == h_id:
            return h
    return None

def get_house_occupants(humans_list, house_uuid):
    return [h for h in humans_list if h.stats["house_uuid"] == house_uuid]

def update_family_logic(human, all_humans):
    if (human.age >= FamilyValues.adult_age and
            human.stats["partner_id"] is None and
            human.money >= FamilyValues.marriage_money_req and
            human.stats["energy"] >= FamilyValues.marriage_energy_req and
            human.status == "idle"):

        potential_partners = [
            p for p in all_humans
            if p.h_id != human.h_id
               and p.age >= FamilyValues.adult_age
               and p.stats["partner_id"] is None
               and p.stats["gender"] != human.stats["gender"]
               and p.money >= FamilyValues.marriage_money_req
               and p.stats["energy"] >= FamilyValues.marriage_energy_req
        ]

        if potential_partners:
            partner = random.choice(potential_partners)
            human.stats["partner_id"] = partner.h_id
            partner.stats["partner_id"] = human.h_id
            human.stats["house_uuid"] = partner.stats["house_uuid"]

    if human.stats["partner_id"]:
        partner = get_human_by_id(all_humans, human.stats["partner_id"])

        if partner:
            if human.stats["gender"] == "female":
                combined_money = human.money + partner.money
                current_house = House.houses.get(human.stats["house_uuid"])
                occupants_count = len(get_house_occupants(all_humans, human.stats["house_uuid"]))

                if combined_money >= FamilyValues.house_build_cost and (current_house is None or occupants_count > 2):
                    if build_family_house(human, partner):
                        human.money -= (FamilyValues.house_build_cost / 2)
                        partner.money -= (FamilyValues.house_build_cost / 2)

                if (FamilyValues.adult_age <= human.age <= FamilyValues.max_reproduce_age and
                        FamilyValues.adult_age <= partner.age <= FamilyValues.max_reproduce_age):

                    if human.stats.get("reproduction_cooldown", 0) <= 0 and partner.stats.get("reproduction_cooldown",
                                                                                              0) <= 0:
                        if human.stats.get("children_count", 0) < FamilyValues.max_children:
                            if current_house and occupants_count < current_house.capacity:
                                if random.random() < FamilyValues.reproduce_chance:
                                    human.stats["children_count"] = human.stats.get("children_count", 0) + 1
                                    partner.stats["children_count"] = partner.stats.get("children_count", 0) + 1

                                    # Setze den Cooldown auf 1 bis 3 Jahre für beide Partner
                                    cooldown = random.randint(1, 3)
                                    human.stats["reproduction_cooldown"] = cooldown
                                    partner.stats["reproduction_cooldown"] = cooldown

                                    child_gen = max(human.stats["generation"], partner.stats["generation"]) + 1
                                    create_human_instance(
                                        type(human),
                                        human.x, human.y,
                                        human.stats["house_uuid"],
                                        generation=child_gen,
                                        parents=[human.h_id, partner.h_id]
                                    )
                                    name = human.stats.get("name", "Unknown")
                                    name2 = partner.stats.get("name", "Unknown")
                                    Logger.log("[Human]", f"Et barn blev født af {name} og {name2}.")

def build_family_house(human1, human2):
    area = FamilyValues.new_house_capacity * 12
    max_attempts = 10

    for _ in range(max_attempts):
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
            new_house = House.create_house(x, y, x2, y2, FamilyValues.new_house_capacity)
            human1.stats["house_uuid"] = new_house.house_id
            human2.stats["house_uuid"] = new_house.house_id

            name = human1.stats.get("name", "Unknown")
            name2 = human2.stats.get("name", "Unknown")

            Logger.log("[House]", f"Et nyt hus blev bygget for {name} og {name2}.")
            return True

    return False