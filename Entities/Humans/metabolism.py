from Entities.office import Office
from Entities.shop import Shop
from config import ConfigValues, FamilyValues, StartValues

def get_parent(all_humans, parent_id):
    for h in all_humans:
        if h.h_id == parent_id:
            return h
    return None

def update_human_metabolism(human, all_humans):
    if human.status != "eating":
        human.stats["nutrition"] -= 0.05

    if human.stats["nutrition"] <= 0:
        human.die()
        return

    is_hungry = human.stats["nutrition"] < 60

    is_busy_sleeping = human.status == "sleeping" or "goto_home" in human.tasks

    if not is_busy_sleeping:
        if human.age < FamilyValues.adult_age:
            if is_hungry and human.money < ConfigValues.mealMinBudget:
                for parent_id in human.stats.get("parents", []):
                    parent = get_parent(all_humans, parent_id)
                    needed_money = ConfigValues.mealMinBudget - human.money
                    if parent and parent.money > needed_money + 10:
                        parent.money -= needed_money
                        human.money += needed_money
                        break
        else:
            if human.money <= ConfigValues.workStartThreshold and human.status not in ["working", "searching_work",
                                                                                       "going_to_work"]:
                target_work = Office.get_nearest_office(human.x, human.y)
                if target_work:
                    human.tasks["goto_work"] = target_work.office_id
                    human.status = "searching_work"

        if is_hungry and "goto_shop" not in human.tasks and human.status != "eating":
            if human.money >= ConfigValues.mealMinBudget:
                if "goto_work" in human.tasks:
                    del human.tasks["goto_work"]

                target_shop = Shop.get_nearest_shop(human.x, human.y)
                if target_shop:
                    human.tasks["goto_shop"] = target_shop.shop_id
                    human.status = "searching_food"

    if human.status == "eating":
        human.stats["nutrition"] += 5
        human.money -= ConfigValues.eatingCostPerTick
        if human.stats["nutrition"] >= 90:
            human.status = "idle"
            if "goto_shop" in human.tasks:
                del human.tasks["goto_shop"]

    if human.status == "working":
        human.money += ConfigValues.hourlyWage
        human.stats["energy"] -= 0.005

        if human.money >= ConfigValues.mealMinBudget and human.stats["nutrition"] < 60:
            target_shop = Shop.get_nearest_shop(human.x, human.y)
            if target_shop:
                human.tasks["goto_shop"] = target_shop.shop_id
                human.status = "searching_food"
                if "goto_work" in human.tasks:
                    del human.tasks["goto_work"]

        if human.money >= ConfigValues.targetSavings:
            if "goto_work" in human.tasks:
                del human.tasks["goto_work"]
            human.status = "idle"