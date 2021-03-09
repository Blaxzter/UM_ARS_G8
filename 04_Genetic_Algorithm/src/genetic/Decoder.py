import numpy as np
from genetic.Genome import Genome
from simulator.Sensors import Sensors
import utils.Constants as Const

"""
Author Guillaume Franzoni Darnois & Frederic Abraham
"""

# def robot_decoder(genome: Genome, sensors: Sensors, prev_hidden: np.ndarray, prev_rotation: float) -> (float, float):
#
#     input_nn = np.array([sensor.length for sensor in sensors.sensors] + [value[0] for value in prev_hidden] + [1]).reshape(1, Const.INPUT_SIZE)
#
#     # Input -> Hidden
#     weights_input = np.array([genome.genes[i] for i in range(Const.INPUT_WEIGHTS_SIZE)]).reshape(Const.HIDDEN_SIZE, Const.INPUT_SIZE)
#     hidden_nn = np.tanh(np.dot(input_nn, weights_input.T) ).reshape(1, Const.HIDDEN_SIZE)
#
#     # Hidden -> Output
#     weights_hidden = np.array([genome.genes[i] for i in range(Const.INPUT_WEIGHTS_SIZE, Const.INPUT_WEIGHTS_SIZE + Const.HIDDEN_WEIGHTS_SIZE)]).reshape(Const.OUTPUT_SIZE, Const.HIDDEN_SIZE)
#     output_nn = np.tanh(np.dot(hidden_nn + [1], weights_hidden.T)) * Const.MAX_SPEED
#
#     velocity = output_nn.reshape(2, 1)
#
#     return velocity, hidden_nn.reshape(Const.HIDDEN_SIZE, 1)

# # Decoder with prev rotation
def robot_decoder(genome: Genome, sensors: Sensors, prev_hidden: np.ndarray, prev_rotation: float) -> (float, float):

    input_nn = np.array([sensor.length for sensor in sensors.sensors] + [value[0] for value in prev_hidden] + [prev_rotation] + [1]).reshape(1, Const.INPUT_SIZE)

    # Input -> Hidden
    weights_input = np.array([genome.genes[i] for i in range(Const.INPUT_WEIGHTS_SIZE)]).reshape(Const.HIDDEN_SIZE, Const.INPUT_SIZE)
    hidden_nn = np.tanh(np.dot(input_nn, weights_input.T) ).reshape(1, Const.HIDDEN_SIZE)

    # Hidden -> Output
    weights_hidden = np.array([genome.genes[i] for i in range(Const.INPUT_WEIGHTS_SIZE, Const.INPUT_WEIGHTS_SIZE + Const.HIDDEN_WEIGHTS_SIZE)]).reshape(Const.OUTPUT_SIZE, Const.HIDDEN_SIZE)
    output_nn = np.tanh(np.dot(hidden_nn + [1], weights_hidden.T)) * Const.MAX_SPEED

    velocity = output_nn.reshape(2, 1)

    return velocity, hidden_nn.reshape(Const.HIDDEN_SIZE, 1)


# def robot_decoder(genome: Genome, sensors: Sensors, prev_hidden: np.ndarray) -> (float, float):
#     input_nn = np.array([sensor.length for sensor in sensors.sensors] + [value[0] for value in prev_hidden]).reshape(1, Const.INPUT_SIZE)
#     input_nn = np.append(input_nn, [1])  # Add the bias
#     # Input -> Hidden
#     weights_input = np.array([genome.genes[i] for i in range(Const.INPUT_WEIGHTS_SIZE)]).reshape(Const.HIDDEN_SIZE, Const.INPUT_SIZE + 1)
#     hidden_nn = np.tanh(np.dot(input_nn, weights_input.T)).reshape(1, Const.HIDDEN_SIZE)
#     hidden_nn = np.append(hidden_nn, [1])  # Add the bias
#
#     # Hidden -> Output
#     weights_hidden = np.array([genome.genes[i] for i in range(Const.INPUT_WEIGHTS_SIZE, Const.INPUT_WEIGHTS_SIZE + Const.HIDDEN_WEIGHTS_SIZE)]).reshape(Const.OUTPUT_SIZE, Const.HIDDEN_SIZE + 1)
#     output_nn = np.tanh(np.dot(hidden_nn, weights_hidden.T)) * Const.MAX_SPEED
#
#     velocity = output_nn.reshape(2, 1)
#
#     return velocity, hidden_nn[0:Const.HIDDEN_SIZE].reshape(Const.HIDDEN_SIZE, 1)
