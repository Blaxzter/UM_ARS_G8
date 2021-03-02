import numpy as np
from src.genetic.Genome import Genome
from src.simulator.Sensors import Sensors
from src.utils.Constants import *

"""
Author Guillaume Franzoni Darnois & Frederic Abraham
"""


def robot_decoder(genome: Genome, sensors: Sensors, prev_hidden: np.ndarray) -> (float, float):

    input_nn = np.array([sensor.length for sensor in sensors.sensors] + [value[0] for value in prev_hidden]).reshape(1, INPUT_SIZE)

    # Input -> Hidden
    weights_input = np.array([genome.genes[i] for i in range(INPUT_WEIGHTS_SIZE)]).reshape(HIDDEN_SIZE, INPUT_SIZE)
    hidden_nn = sigmoid(np.dot(input_nn, weights_input.T)).reshape(1, HIDDEN_SIZE)

    # Hidden -> Output
    weights_hidden = np.array([genome.genes[i] for i in range(INPUT_WEIGHTS_SIZE, INPUT_WEIGHTS_SIZE + HIDDEN_WEIGHTS_SIZE)]).reshape(OUTPUT_SIZE, HIDDEN_SIZE)
    output_nn = sigmoid(np.dot(hidden_nn, weights_hidden.T))

    velocity = output_nn.reshape(2, 1)

    return velocity, hidden_nn.reshape(HIDDEN_SIZE, 1)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))
