import datetime

class Preview:
    # i minutter, hvis -1 så er det deaktiveret
    generate_picture = -1
    picture_width = 400
    picture_height = 300
    live_preview = True
    live_stats = True
    ignore_logger = ["[Tick]"]

class StartValues:
    # startværdier, bliver genereret tilfældigt på simulationskortet
    startWithHumans = 20
    startWithHouses = 8
    startWithLibraries = 0
    startWithShops = 1
    startWithOffices = 1

    started = datetime.datetime.now()
    daytime = True

class ConfigValues:
    hourlyWage = 2
    eatingCostPerTick = 1
    mealMinBudget = 20
    workStartThreshold = 40
    targetSavings = 250

class EconomyValues:
    new_office_capacity = 20
    shop_area_per_customer = 10

class FamilyValues:
    adult_age = 20
    max_reproduce_age = 55
    marriage_money_req = 40
    marriage_energy_req = 50
    house_build_cost = 150
    new_house_capacity = 5
    reproduce_chance = 0.15
    max_children = 4