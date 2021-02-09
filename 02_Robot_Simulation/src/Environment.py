import numpy as np

from Line import Line
from src.Constatns import padding, width, height


class Environment:
    def __init__(self):
        self.environment = [
            Line(start=np.array([padding, padding]), end=np.array([width - padding, padding])),
            Line(start=np.array([width - padding, padding]), end=np.array([width - padding, height - padding])),
            Line(start=np.array([width - padding, height - padding]), end=np.array([padding, height - padding])),
            Line(start=np.array([padding, height - padding]), end=np.array([padding, padding])),
            Line(start=np.array([69, 69]), end=np.array([169, 196])),
        ]

    def draw(self, screen):
        for line in self.environment:
            line.draw(screen)

    def collides(self, start: np.ndarray, end: np.ndarray):
        pass