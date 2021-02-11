import numpy as np
import pygame

from src.Constants import robot_radius, epsilon

line_color = (0, 128, 255)


class Line:
    def __init__(self, start_x: float, start_y: float, end_x: float, end_y: float):
        self.start_x: float = start_x
        self.start_y: float = start_y
        self.end_x: float = end_x
        self.end_y: float = end_y

        self.start = np.array([start_x, start_y]).reshape((2, 1))
        self.end = np.array([end_x, end_y]).reshape((2, 1))

        self.vec = np.array(self.end - self.start).reshape((2, 1))
        self.nvec = (self.vec / np.linalg.norm(self.vec)).reshape((2, 1))

        self.col_start: np.ndarray = self.start + (self.nvec * -1) * robot_radius
        self.col_end: np.ndarray = self.end + self.nvec * robot_radius

        self.col_start_x: float = self.col_start[0].item()
        self.col_start_y: float = self.col_start[1].item()
        self.col_end_x: float = self.col_end[0].item()
        self.col_end_y: float = self.col_end[1].item()

        self.length = np.linalg.norm(self.vec)
        self.pyStart = pygame.Vector2(self.start[0], self.start[1])
        self.pyEnd = pygame.Vector2(self.end[0], self.end[1])
        self.angle = self.compute_slope()

    def is_on(self, point):
        crossproduct = (point[1].item() - self.col_start_y) * (self.col_end_x - self.col_start_x) - (point[0].item() - self.col_start_x) * (self.col_end_y - self.col_start_y)

        # compare versus epsilon for floating point values, or != 0 if using integers
        if abs(crossproduct) > epsilon:
            return False

        dotproduct = (point[0].item() - self.col_start_x) * (self.col_end_x - self.col_start_x) + (point[1].item() - self.col_start_y) * (self.col_end_y - self.col_start_y)
        if dotproduct < 0:
            return False

        squaredlengthba = (self.col_end_x - self.col_start_x) * (self.col_end_x - self.col_start_x) + (self.col_end_y - self.col_start_y) * (self.col_end_y - self.col_start_y)
        if dotproduct > squaredlengthba:
            return False

        return True

    def __str__(self):
        return f'({self.start_x}, {self.start_y}) ({self.end_x}, {self.end_y})'

    def draw(self, screen):
        pygame.draw.line(screen, line_color, self.pyStart, self.pyEnd, 2)

    def compute_slope(self):
        return (self.start[1] - self.end[1]) / (self.start[0] - self.end[0]) if (self.start[0] - self.end[0]) != 0 else np.inf
