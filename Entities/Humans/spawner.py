# Entities/Humans/spawner.py
import uuid
import random

from Managers.name_manager import NameManager


def create_human_instance(cls, x, y, house_uuid, generation=1, parents=None):
    h_id = str(uuid.uuid4())
    age = 0
    gender = random.choice(["male", "female"])
    sl = random.uniform(1.5, 3.0)

    stats = {
        "name": NameManager.get_random_name(gender),
        "house_uuid": house_uuid,
        "step_length": sl,
        "nutrition": 100,
        "energy": 100,
        "sleep_debt": 0.0,
        "gender": gender,
        "partner_id": None,
        "generation": generation,
        "parents": parents if parents else [],
        "children_count": 0,
        "reproduction_cooldown": 0
    }
    needs = {}
    tasks = {}

    new_human = cls(h_id, x, y, age, stats, needs, tasks, money=0)
    cls.humans.append(new_human)
    return new_human


def spawn_human_instance(cls, x, y, house_uuid):
    h_id = str(uuid.uuid4())
    age = random.randint(18, 30)
    gender = random.choice(["male", "female"])
    sl = random.uniform(1.5, 3.0)

    stats = {
        "name": NameManager.get_random_name(gender),
        "house_uuid": house_uuid,
        "step_length": sl,
        "nutrition": random.uniform(60, 100),
        "energy": random.uniform(60, 100),
        "sleep_debt": 0.0,
        "gender": gender,
        "partner_id": None,
        "generation": 1,
        "parents": [],
        "children_count": 0,
        "reproduction_cooldown": 0
    }
    needs = {}
    tasks = {}

    new_human = cls(h_id, x, y, age, stats, needs, tasks, money=50)
    cls.humans.append(new_human)


def spawn_humans_batch(cls, houses, humans):
    for i in range(humans):
        house_index = i % len(houses)
        my_house = houses[house_index]

        min_x = my_house.x
        max_x = my_house.x2
        min_y = my_house.y
        max_y = my_house.y2

        spawn_x = random.randint(min_x, max_x)
        spawn_y = random.randint(min_y, max_y)

        spawn_human_instance(cls, spawn_x, spawn_y, my_house.house_id)