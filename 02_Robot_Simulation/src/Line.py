import numpy as np
import pygame

line_color = (0, 128, 255)


class Line:
    def __init__(self, start: np.ndarray, end: np.ndarray):
        self.start: np.ndarray = start.reshape((2, 1))
        self.end: np.ndarray = end.reshape((2, 1))
        self.vec = np.array(end - start).reshape((2,1))
        self.nvec = (self.vec / np.linalg.norm(self.vec)).reshape((2, 1))
        self.pyStart = pygame.Vector2(self.start[0], self.start[1])
        self.pyEnd = pygame.Vector2(self.end[0], self.end[1])
        self.angle = self.compute_slope()

    def draw(self, screen):
        pygame.draw.line(screen, line_color, self.pyStart, self.pyEnd, 2)

    def compute_slope(self):
        return (self.start[1] - self.end[1]) / (self.start[0] - self.end[0]) if (self.start[0] - self.end[0]) != 0 else np.inf
