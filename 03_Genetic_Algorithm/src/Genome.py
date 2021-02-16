from typing import List, Dict

import numpy as np
import Constants as Const


class Genome:
    def __init__(self):
        self.genes: List[Dict[float, float]] = self.init_genome()

    @staticmethod
    def init_genome():
        return [{
            'd_v_l': np.random.choice([-1, 1]) * Const.robot_velocity_steps,
            'd_v_r': np.random.choice([-1, 1]) * Const.robot_velocity_steps
        } for _ in range(Const.individuals_life_steps)]