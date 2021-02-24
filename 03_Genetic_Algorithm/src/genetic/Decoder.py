import numpy as np

from src.genetic.Genome import Genome


def robot_decoder(genome: Genome) -> (float, float):
    # TODO implement the neural network that decodes the genome into a velocity

    velocity = np.random.uniform(low = 1, high = 2, size = (2, 1))

    return velocity[0].item(), velocity[1].item()
