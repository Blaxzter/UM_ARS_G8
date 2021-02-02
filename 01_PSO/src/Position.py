from numpy import ndarray


class Position:
    def __init__(self, vec: ndarray):
        self.vec: ndarray = vec
