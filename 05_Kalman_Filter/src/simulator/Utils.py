import numpy as np
import pygame


def get_pygame_point(pos: np.ndarray) -> pygame.Vector2:
    return pygame.Vector2(pos[0], pos[1])
