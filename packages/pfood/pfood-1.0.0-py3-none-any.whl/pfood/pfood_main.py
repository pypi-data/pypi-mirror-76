import os
import random
import re


class PFood:
    """Read main foods file and store all of them in array for later use"""

    def __init__(self) -> None:
        super().__init__()
        file = open(os.path.dirname(os.path.realpath(__file__)) + "/../list.txt", "r")
        foods = []
        for food in file:
            foods.append(re.search(r"\d+-\s(.+)", food).group(1))
        self.foods = foods

    def print_random(self, count: int):
        for _ in range(count):
            print(random.choice(self.foods))

    def print_all(self):
        for food in self.foods:
            print(food)
