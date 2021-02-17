from random import randint
from typing import List, Dict

import numpy as np
import Constants as Const


class Genome:
    def __init__(self):
        self.genes: List[Dict[float, float]] = self.init_genome()

    def crossover(self, other):
        one_point = randint(0, Const.individuals_life_steps)
        for i in range(Const.individuals_life_steps):
            if i < one_point:
                temp = self.genes[i]
                self.genes[i] = other.genes[i]
                other.genes[i] = temp

    def mutation(self):
        for i in range(Const.individuals_life_steps):
            if np.random.uniform(low=0, high=1) < 0.5:
                self.genes[i] = {
                    'd_v_l': np.random.choice([-1, 0, 1]) * Const.robot_velocity_steps,
                    'd_v_r': np.random.choice([-1, 0, 1]) * Const.robot_velocity_steps
                }

    @staticmethod
    def init_genome():
        return [{
            'd_v_l': np.random.choice([-1, 0, 1]) * Const.robot_velocity_steps,
            'd_v_r': np.random.choice([-1, 0, 1]) * Const.robot_velocity_steps
        } for _ in range(Const.individuals_life_steps)]
