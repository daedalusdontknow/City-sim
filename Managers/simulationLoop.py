import datetime
import os
import math
import random

from Entities.buildings import Building
from Entities.house import House
from Entities.office import Office
from Entities.shop import Shop
from Entities.human import Human

from Managers.logger import Logger
from Managers.saveSimulation import Saver

from config import Preview, StartValues

class Loop:

    var = 3600

    FULL_DAY = 1800
    ONE_HOUR = int(FULL_DAY / 24)
    TICKS_PER_YEAR = 21600

    start_day = 6 * ONE_HOUR
    end_day = 20 * ONE_HOUR

    @staticmethod
    def tick():
        if Loop.var % 600 == 0:
            running_since = datetime.datetime.now() - StartValues.started
            Logger.log("[Tick]", f"running for {running_since} (Ticks: {Loop.var}) its {'daytime' if StartValues.daytime else 'nighttime'} now")

        if Loop.var % Loop.TICKS_PER_YEAR == 0:
            Logger.log("[Tick]", f"a year passed")
            Human.update_age()

        current_time_in_day = Loop.var % Loop.FULL_DAY

        if Loop.start_day <= current_time_in_day < Loop.end_day: StartValues.daytime = True
        else: StartValues.daytime = False

        Human.update_humans()

        Loop.var += 1

    @staticmethod
    def start():
        StartValues.started = datetime.datetime.now()
        if len(os.listdir("saves")) != 0:

            valid_sims = {}
            num = 0

            Logger.log("[Main]", "Du kan fortsætte med følgende simulationer:")
            with os.scandir('saves') as d:
                for e in d:
                    valid_sims[num] = e.name
                    print(f"{num}. {e.name}")
                    num += 1

            print(f"{num}. start ny simulation")
            ci = int(input())

            if ci == num: Loop.startnew()
            else: Saver.load(valid_sims[ci])

        else: Loop.startnew()

    @staticmethod
    def startnew():

        # spawn houses
        houses = House.spawn_houses(StartValues.startWithHouses, StartValues.startWithHumans)

        # spawn humans
        Human.spawn_humans(houses, StartValues.startWithHumans)

        # spawn shops
        Shop.spawn_shops(StartValues.startWithShops)

        # spawn offices
        Office.spawn_offices(StartValues.startWithOffices, 10)

        Logger.log("[Main]", "startede ny simulation")