import numpy as np
import pygame

from src.Constatns import width, height
from src.Environment import Environment
from src.Robot import Robot

import Constatns as Const

class Simulator:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((width, height))
        self.environment = Environment()
        start_location = np.array([Const.start_x, Const.start_y], dtype=float).reshape((2, 1))
        self.robot = Robot(start_location)
        self.keys = [
            dict(key_code=pygame.K_w, callback=self.robot.increase_left, pressed=False),
            dict(key_code=pygame.K_s, callback=self.robot.decrease_left, pressed=False),
            dict(key_code=pygame.K_o, callback=self.robot.increase_right, pressed=False),
            dict(key_code=pygame.K_l, callback=self.robot.decrease_right, pressed=False),
            dict(key_code=pygame.K_x, callback=self.robot.stop, pressed=False),
            dict(key_code=pygame.K_a, callback=self.robot.rotate_left, pressed=False),
            dict(key_code=pygame.K_d, callback=self.robot.rotate_right, pressed=False),
        ]
        self.done = False
        pygame.init()

    def start(self):
        while not self.done:
            self.pygame_defaults()

            self.update()
            self.draw()

            self.clock.tick(60)

    def update(self):
        self.get_key_update()
        self.do_robot_update()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.environment.draw(self.screen)
        self.robot.draw(self.screen)
        pygame.display.flip()

    def get_key_update(self):
        pressed = pygame.key.get_pressed()
        for key in self.keys:
            if pressed[key['key_code']]:
                if not key['pressed']:
                    key['callback']()
                    key['pressed'] = True
            else:
                key['pressed'] = False

    def pygame_defaults(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

    def do_robot_update(self):
        self.robot.update(self.environment)
        pass
