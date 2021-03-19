import numpy as np
import simulator.Constants as Const
from simulator.MathUtils import covariance_matrix


class KalmanFilter:

    def __init__(self, d_t, theta):

        self.A = np.identity(3)
        self.B = np.array([d_t * -np.cos(theta), 0,
                           d_t * -np.sin(theta), 0,
                           0, d_t]).reshape(3, 2)
        self.C = np.identity(3)

        # Noise matrices
        self.R = np.array([
            0.010, 0, 0,
            0, 0.010, 0,
            0, 0, 0.100
        ]).reshape(3, 3)
        self.Q = np.array([
            0.010, 0, 0,
            0, 0.010, 0,
            0, 0, 0.100
        ]).reshape(3, 3)

    def kalman_filter(self, mu, sigma, u, z):
        # NB: For the dot product the order doesn't count

        # Prediction
        new_mu = self.A.dot(mu) + self.B.dot(u)
        new_sigma = self.A.dot(sigma.dot(self.A.T)) + self.R

        # Correction
        if z is not None:
            # check if there are 3 landmarks inside the range
            # triangulation()
            K = np.dot(new_sigma, self.C.T).dot(np.linalg.inv(self.C.dot(new_sigma.dot(self.C.T)) + self.Q))
            new_mu = new_mu + K.dot(z - self.C.dot(new_mu))
            new_sigma = (np.identity(3) - K.dot(self.C)).dot(new_sigma)

        return new_mu, new_sigma

    def update_matrices(self, d_t, theta):
        self.B = np.array([
            d_t * -np.cos(theta), 0,
            d_t * -np.sin(theta), 0,
            0,                   d_t
        ]).reshape(3, 2)


