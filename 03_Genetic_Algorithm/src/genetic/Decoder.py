import numpy as np

from src.genetic.Genome import Genome
from src.simulator.Sensors import Sensors
from src.utils.Constants import NUMBER_OF_SENSORS, VALUES_PER_AXIS


def optimization_decoder(genome: Genome) -> np.ndarray:
    return np.sum(np.array(genome.genes).reshape((int(len(genome.genes)/VALUES_PER_AXIS), VALUES_PER_AXIS)), axis=1) / VALUES_PER_AXIS


def robot_decoder(genome: Genome, sensors: Sensors) -> (float, float):
    # TODO The velocity should feed back into the NN like a RNN 

    input_nn = np.array([sensor.length for sensor in sensors.sensors]).reshape(1, NUMBER_OF_SENSORS)
    weights_input = np.array([gene for gene in genome.genes]).reshape(2, NUMBER_OF_SENSORS)

    output = sigmoid(np.dot(input_nn, weights_input.T))

    velocity = output.reshape(2, 1)

    return velocity[0].item(), velocity[1].item()


def sigmoid(x):
    return 1 / (1 + np.exp(-x))
