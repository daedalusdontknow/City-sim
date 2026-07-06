import random
import os
from Managers.logger import Logger

class NameManager:
    male_names = []
    female_names = []

    @classmethod
    def load_names(cls):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        male_path = os.path.join(base_dir, "resources", "male.txt")
        female_path = os.path.join(base_dir, "resources", "female.txt")

        if os.path.exists(male_path):
            with open(male_path, "r", encoding="utf-8") as f:
                cls.male_names = [line.strip() for line in f.readlines()[7:] if line.strip()]
        else:
            Logger.log("[Error]", f"Fil ikke fundet: {male_path}")

        if os.path.exists(female_path):
            with open(female_path, "r", encoding="utf-8") as f:
                cls.female_names = [line.strip() for line in f.readlines()[7:] if line.strip()]
        else:
            Logger.log("[Error]", f"Fil ikke fundet: {female_path}")

    @classmethod
    def get_random_name(cls, gender):
        if gender == "male" and cls.male_names:
            return random.choice(cls.male_names)
        elif gender == "female" and cls.female_names:
            return random.choice(cls.female_names)
        return "Unknown"