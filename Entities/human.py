import random

from Entities.house import House
from Managers.logger import Logger

from Entities.Humans.movement import move_human
from Entities.Humans.metabolism import update_human_metabolism
from Entities.Humans.energy import update_human_energy
from Entities.Humans.spawner import create_human_instance, spawn_human_instance, spawn_humans_batch
from Entities.Humans.family import update_family_logic
from Entities.office import Office
from Entities.shop import Shop
from config import FamilyValues


class Human:
    humans = []

    def __init__(self, h_id, x, y, age, stats, needs, tasks, money):
        self.h_id = h_id
        self.x = x
        self.y = y
        self.age = age
        self.stats = stats
        self.needs = needs
        self.tasks = tasks
        self.status = "sleeping"
        self.money = money
        self.internal_tick_counter = random.randint(1, 60)

    @staticmethod
    def update_humans():
        for human in Human.humans:
            human.internal_tick_counter += 1

            move_human(human)

            if human.internal_tick_counter % 10 == 0:
                update_human_metabolism(human, Human.humans)

            if human.internal_tick_counter % 50 == 0:
                update_family_logic(human, Human.humans)

            if human.internal_tick_counter % 100 == 0:
                House.cleanup_empty_houses(Human.humans)

                total_pop = len(Human.humans)
                Shop.check_and_expand(total_pop)

                adults = sum(1 for h in Human.humans if h.age >= FamilyValues.adult_age)
                Office.check_and_expand(adults)

            update_human_energy(human)

    def die(self):
        heirs = [h for h in Human.humans if
                 h.h_id == self.stats.get("partner_id") or self.h_id in h.stats.get("parents", [])]

        if heirs and self.money > 0:
            split_money = self.money / len(heirs)
            for heir in heirs:
                heir.money += split_money

        if self in Human.humans:
            Human.humans.remove(self)
        name = self.stats.get("name", "Unknown")
        Logger.log("[Death]", f"Menneske {name} døde i en alder af {self.age}.")

    @staticmethod
    def update_age():
        for human in Human.humans:
            human.age += 1

            if human.stats.get("reproduction_cooldown", 0) > 0:
                human.stats["reproduction_cooldown"] -= 1

            if human.age > 70:
                chance_to_die = (human.age - 70) * 0.05
                if random.random() < chance_to_die:
                    human.die()

    @classmethod
    def get_human_count(cls):
        return len(cls.humans)

    @classmethod
    def create_human(cls, x, y, parent_stats):
        create_human_instance(cls, x, y, parent_stats)

    @classmethod
    def spawn_human(cls, x, y, house_uuid):
        spawn_human_instance(cls, x, y, house_uuid)

    @classmethod
    def spawn_humans(cls, houses, humans):
        spawn_humans_batch(cls, houses, humans)