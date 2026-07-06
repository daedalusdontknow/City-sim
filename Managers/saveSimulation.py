import datetime
import json
import os
import tempfile

from Entities.house import House
from Entities.human import Human
from Entities.office import Office
from Entities.shop import Shop
from Managers.logger import Logger
from config import StartValues


class Saver:
    SAVE_DIR = "saves"

    @staticmethod
    def _build_snapshot():
        return {
            "daytime": StartValues.daytime,
            "houses": [h.__dict__.copy() for h in House.houses.values()],
            "shops": [s.__dict__.copy() for s in Shop.shops.values()],
            "offices": [o.__dict__.copy() for o in Office.offices.values()],
            "humans": [h.__dict__.copy() for h in Human.humans]
        }

    @staticmethod
    def save(filename=None):
        if filename is None:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"savegame_{timestamp}.json"

        if not os.path.exists(Saver.SAVE_DIR):
            os.makedirs(Saver.SAVE_DIR)

        filepath = os.path.join(Saver.SAVE_DIR, filename)
        try:
            data = Saver._build_snapshot()

            fd, temp_path = tempfile.mkstemp(prefix=".tmp_save_", suffix=".json", dir=Saver.SAVE_DIR)
            try:
                with os.fdopen(fd, 'w') as f:
                    json.dump(data, f, indent=4)

                os.replace(temp_path, filepath)
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

            Logger.log("[Saver]", f"Simulationen blev gemt: {filename}")
        except Exception as e:
            Logger.log("[Error]", f"Fejl ved at gemme: {e}")

    @staticmethod
    def load(filename):
        filepath = os.path.join(Saver.SAVE_DIR, filename)

        if not os.path.exists(filepath):
            Logger.log("[Error]", f"Kunne ikke finde filen: {filename}")
            return

        try:
            with open(filepath, 'r') as f:
                data = json.load(f)

            Human.humans.clear()
            House.houses.clear()
            Shop.shops.clear()
            Office.offices.clear()

            StartValues.daytime = data["daytime"]

            for h_data in data["houses"]:
                new_house = House.__new__(House)
                new_house.__dict__.update(h_data)

                House.houses[new_house.house_id] = new_house

            for s_data in data["shops"]:
                new_shop = Shop.__new__(Shop)
                new_shop.__dict__.update(s_data)

                Shop.shops[new_shop.shop_id] = new_shop

            for o_data in data["offices"]:
                new_office = Office.__new__(Office)
                new_office.__dict__.update(o_data)

                Office.offices[new_office.office_id] = new_office

            for h_data in data["humans"]:
                new_human = Human.__new__(Human)
                new_human.__dict__.update(h_data)

                new_human.tasks = {}
                new_human.status = "idle"

                Human.humans.append(new_human)

            Logger.log("[Saver]", f"Simulation {filename} blev indlæst.")
            os.remove(filepath)

        except Exception as e:
            Logger.log("[Error]", f"Fejl ved indlæsning: {e}")