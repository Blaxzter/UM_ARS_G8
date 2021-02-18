from random import randint
from typing import List, Dict

import numpy as np
import Constants as Const


class Genome:
    def __init__(self):
        self.genes: List[Dict[str, float]] = self.init_genome()

    def crossover(self, partner):
        first_point = randint(0, Const.individuals_life_steps)
        new_genes = []
        for i in range(Const.individuals_life_steps):
            if first_point < i:
                new_genes.append(self.genes[i])
            else:
                new_genes.append(partner.genes[i])
        return new_genes

    def mutation(self):
        for i in range(Const.individuals_life_steps):
            if np.random.uniform(low=0, high=1) < 0.08:
                self.genes[i] = {
                    'd_v_l': np.random.choice([-1, 0, 1]) * Const.robot_velocity_steps,
                    'd_v_r': np.random.choice([-1, 0, 1]) * Const.robot_velocity_steps
                }

    def extend_genome(self):
        self.genes.extend([{
                'd_v_l': np.random.choice([-1, 0, 1]) * Const.robot_velocity_steps,
                'd_v_r': np.random.choice([-1, 0, 1]) * Const.robot_velocity_steps
            } for _ in range(Const.life_update)])

    @staticmethod
    def init_genome():
        return [{
            'd_v_l': np.random.choice([-1, 0, 1]) * Const.robot_velocity_steps,
            'd_v_r': np.random.choice([-1, 0, 1]) * Const.robot_velocity_steps
        } for _ in range(Const.individuals_life_steps)]
