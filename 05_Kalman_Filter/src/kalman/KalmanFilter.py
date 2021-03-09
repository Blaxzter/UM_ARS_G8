import numpy as np

class KalmanFilter:

    def __init__(self):
        # TODO figure out the correct initializations from the slide

        self.A = np.identity(3)
        self.B = np.identity(3)

    def kalman_filter(self, mu, sigma, u, z):
        pass