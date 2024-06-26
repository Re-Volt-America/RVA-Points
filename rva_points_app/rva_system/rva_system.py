import yaml

from rva_points_app.common import *
from rva_points_app.exception import *


class RVASystem:
    def __init__(self):
        self.category_class_number = None
        self.allow_mystery = False

        """
        Maps the difference of car classes between session and racer to the correspondent bonus multiplier.  When a
        session category class is higher than the class of the car a racer used, a racer's score gets multiplied
        by this bonus (ref: https://rva.lat/points)
        """
        self.BONUSES_PER_CLASS_DIFF = {
            0: 1.0,
            1: 1.25,
            2: 1.5,
            3: 1.75,
            4: 2,
            5: 2.25
        }
        self.CLASS_NUMBERS_MAP = {
            "rookie": ROOKIE,
            "amateur": AMATEUR,
            "advanced": ADVANCED,
            "semi-pro": SEMI_PRO,
            "pro": PRO,
            "super-pro": SUPER_PRO,
            "random": RANDOM,
            "clockwork": CLOCKWORK
        }
        self.POSITION_SUFFIXES = {
            1: "st",
            2: "nd",
            3: "rd",
            **dict.fromkeys(list(range(4, 17)), "th")
        }
        self.SCORING = {
            1: 15,
            2: 12,
            3: 10,
            4: 7,
            5: 5,
            6: 4,
            7: 2, 8: 2,
            9: 1,
            10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1
        }
        self.BIG_SCORING = {
            1: 20,
            2: 16,
            3: 12,
            4: 10,
            5: 8, 6: 8,
            7: 6,
            8: 4,
            9: 2, 10: 2,
            11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1
        }
        self.NORMALIZER_CONSTANT = 0.1
        self.CARS_INFO = {}

        self.__load_cars()

    def set_category_class_number(self, category_class_number):
        self.category_class_number = category_class_number

    def set_allows_mystery(self, allows_mystery):
        self.allow_mystery = allows_mystery

    def get_car_multiplier(self, car_name):
        car = self.__get_car(car_name)

        if car is not None:
            return car["multiplier"]

        return 0.0

    def get_car_class(self, car_name):
        car = None
        clazz = None
        for car_class in RVGL_CAR_CLASSES_NAMES:
            try:
                car = self.CARS_INFO[car_class][self.__get_car_slug(car_name)]
            except KeyError:
                pass

            if car is not None:
                clazz = car_class
                break
        return clazz

    def get_position_score(self, position, big_scoring):
        if big_scoring:
            return self.BIG_SCORING[position]
        else:
            return self.SCORING[position]

    def get_car_bonus(self, car_name):
        if car_name == MYSTERY_NAME and not self.allow_mystery:
            return None  # Car is mystery & the allow mystery box is unchecked, therefore invalid

        if self.category_class_number == RANDOM:
            return 1.0  # The current category is Random, therefore all cars are valid & bonus is always 1.0

        car_class = self.get_car_class(car_name)
        if car_class is None:
            raise CarNotFound(car_name)

        car_class_number = self.CLASS_NUMBERS_MAP[car_class]

        if self.category_class_number == CLOCKWORK and car_class_number == RANDOM:
            return 1.0  # The current category is Clockwork, and player is using a Clockwork, therefore valid and 1.0
        elif self.category_class_number == CLOCKWORK and car_class_number != CLOCKWORK:
            return None  # The current category is Clockwork, but the player is not using a Clockwork, therefore invalid
        elif self.category_class_number != CLOCKWORK and car_class_number == CLOCKWORK:
            return None  # The current category is not Clockwork, but player is using a Clockwork, therefore invalid

        # RANDOM and CLOCKWORK never make it here, so no side effects!
        car_class_delta = self.category_class_number - car_class_number
        if car_class_delta < 0:
            return None  # Car is above the current category, therefore points are invalid
        else:
            return self.BONUSES_PER_CLASS_DIFF[car_class_delta]

    def get_racer_score(self, racer_entry, race):
        car_bonus = self.get_car_bonus(racer_entry.car)

        if car_bonus is not None:
            final_mult = round(self.get_car_multiplier(racer_entry.car) * car_bonus, 3)
            if final_mult > 4.0:
                final_mult = 4.0
            big_race = len(race.racers) >= 10  # If the race had 10+ people (inclusive) we use the big scoring system.
            racer_score = round(self.get_position_score(racer_entry.position, big_scoring=big_race) * final_mult, 3)

            print_log(f"[{race.track}] {racer_entry.position}{self.POSITION_SUFFIXES[racer_entry.position]}, "
                      f"{racer_entry.car}, "
                      f"Multiplier: {final_mult}, "
                      f"Score: {racer_score}")

            return racer_score

        print_log(f"[{race.track}] {racer_entry.position}{self.POSITION_SUFFIXES[racer_entry.position]}, "
                  f"{racer_entry.car}, "
                  f"Multiplier: Invalid, "
                  f"Score: {0.0}")
        return 0.0  # Car is above the current category's class, therefore points are invalidated

    def __load_cars(self):
        for car_class in RVGL_CAR_CLASSES_NAMES:
            with open(os.path.join(os.getcwd(), "data", "%s.yml" % car_class), encoding="utf8") as fh:
                read_data = yaml.load(fh, Loader=yaml.FullLoader)
                self.CARS_INFO = dict(self.CARS_INFO, **read_data)

    def __get_car(self, car_name):
        car = None
        for car_class in RVGL_CAR_CLASSES_NAMES:
            try:
                car = self.CARS_INFO[car_class][self.__get_car_slug(car_name)]
            except KeyError:
                pass
            if car is not None:
                break
        return car

    @staticmethod
    def __get_car_slug(car):
        return car.lower().replace(" ", "_")
