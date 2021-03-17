import numpy as np
import simulator.Constants as Const

class KalmanFilter:

    def __init__(self, d_t, theta):

        self.A = np.identity(3)
        self.B = np.array([d_t * np.cos(theta), 0,
                           d_t * np.sin(theta), 0,
                           0, d_t]).reshape(3, 2)
        self.C = np.identity(3)

        # Noise matrices
        self.R = np.identity(3) * np.array([
            np.random.normal(scale=Const.GAUSSIAN_SCALE),
            np.random.normal(scale=Const.GAUSSIAN_SCALE),
            np.random.normal(scale=Const.GAUSSIAN_SCALE)]
        ).reshape(3, 1)
        self.Q = np.identity(3) * np.array([
            np.random.normal(scale=Const.GAUSSIAN_SCALE),
            np.random.normal(scale=Const.GAUSSIAN_SCALE),
            np.random.normal(scale=Const.GAUSSIAN_SCALE)]
        ).reshape(3, 1)

    def kalman_filter(self, mu, sigma, u, z):
        # NB: For the dot product the order doesn't count

        # Prediction
        new_mu = self.A.dot(mu) + self.B.dot(u)
        new_sigma = self.A.dot(sigma.dot(self.A.T)) + self.R

        # Correction
        K = np.dot(new_sigma, self.C.T).dot(np.linalg.inv(self.C.dot(new_sigma.dot(self.C.T)) + self.Q))
        corrected_new_mu = new_mu + K.dot(z - self.C.dot(new_mu))
        corrected_new_sigma = (np.identity(3) - K.dot(self.C)).dot(new_sigma)

        return corrected_new_mu, corrected_new_sigma

    def update_matrices(self, d_t, theta):
        self.B = np.array([
            d_t * np.cos(theta), 0,
            d_t * np.sin(theta), 0,
            0,                   d_t
        ]).reshape(3, 2)

        # Noise matrices
        self.R = np.identity(3) * np.array([
            np.random.normal(scale=Const.GAUSSIAN_SCALE),
            np.random.normal(scale=Const.GAUSSIAN_SCALE),
            np.random.normal(scale=Const.GAUSSIAN_SCALE)]
        ).reshape(3, 1)
        self.Q = np.identity(3) * np.array([
            np.random.normal(scale=Const.GAUSSIAN_SCALE),
            np.random.normal(scale=Const.GAUSSIAN_SCALE),
            np.random.normal(scale=Const.GAUSSIAN_SCALE)]
        ).reshape(3, 1)
