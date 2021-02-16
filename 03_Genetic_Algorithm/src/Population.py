import Constants as Const
from src.Robot import Robot


class Population:

    def __init__(self):
        self.individuals = self.init_individuals()

    def update(self, environment):
        for individual in self.individuals:
            individual.apply_genome()
            individual.update(environment)

    def draw(self, screen):
        for individual in self.individuals:
            individual.draw(screen)

    @staticmethod
    def init_individuals():
        return [Robot(Const.start_location) for _ in range(Const.number_of_individuals)]