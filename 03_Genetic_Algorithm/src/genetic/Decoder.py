import numpy as np

from src.genetic.Genome import Genome
from src.simulator.Sensors import Sensors
from src.utils.Constants import NUMBER_OF_SENSORS


def robot_decoder(genome: Genome, sensors: Sensors) -> (float, float):
    # TODO implement the neural network that decodes the genome into a velocity

    input_nn = np.array([sensor.length for sensor in sensors.sensors]).reshape(1, NUMBER_OF_SENSORS)
    weights_input = np.array([gene for gene in genome.genes]).reshape(2, NUMBER_OF_SENSORS)

    output = sigmoid(np.dot(input_nn, weights_input.T))

    velocity = output.reshape(2, 1)

    return velocity[0].item(), velocity[1].item()


def sigmoid(x):
    return 1 / (1 + np.exp(-x))
