# Entities/Humans/energy.py
from config import StartValues
from Entities.house import House


def update_human_energy(human):
    age_penalty = (human.age / 100) * 0.02

    if "sleep_debt" not in human.stats:
        human.stats["sleep_debt"] = 0.0

    if human.status != "sleeping":
        human.stats["energy"] -= (0.02 + age_penalty + human.stats["sleep_debt"])
        human.stats["sleep_debt"] += 0.0002
    else:
        human.stats["sleep_debt"] = max(0.0, human.stats["sleep_debt"] - 0.01)

    is_night = not StartValues.daytime
    is_very_tired = human.stats["energy"] < 40

    wants_to_sleep = is_night or is_very_tired

    if wants_to_sleep:
        if is_at_home(human):
            human.status = "sleeping"
            human.stats["path"] = []  # <--- FIX: Löscht die rote Linie
            if "goto_home" in human.tasks:
                del human.tasks["goto_home"]
        else:
            if human.status not in ["going_home", "walking"]:
                if "goto_shop" in human.tasks: del human.tasks["goto_shop"]
                if "goto_work" in human.tasks: del human.tasks["goto_work"]

                human.status = "walking"
                human.tasks["goto_home"] = True
    else:
        if human.status == "sleeping":
            human.status = "idle"

    if human.status == "sleeping":
        human.stats["energy"] += 0.1

        if human.stats["energy"] >= 100:
            human.stats["energy"] = 100
            if not is_night:
                human.status = "idle"

    if human.stats["energy"] < 0:
        human.stats["energy"] = 0


def is_at_home(human):
    my_house = House.houses.get(human.stats["house_uuid"])
    if my_house:
        return (my_house.x <= human.x <= my_house.x2 and
                my_house.y <= human.y <= my_house.y2)
    return False