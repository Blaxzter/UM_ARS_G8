from concurrent.futures.process import ProcessPoolExecutor
from typing import List, Dict, Callable

import os
import pygame
import numpy as np


from src.simulator.Robot import Robot
from src.utils.Constants import WIDTH, HEIGHT, LIFE_STEPS, FPS, COLORS, DRAW
from src.simulator.Environment import Environment
from src.genetic.Population import Population

class Simulator:
    test = 0

    def __init__(self, display_data: Dict, simulation_time = LIFE_STEPS, gui_enabled = True, stop_callback: Callable = None):

        print(Simulator.test)
        Simulator.test += 1

        self.stop_callback = stop_callback
        self.display_data = display_data
        self.gui_enabled = gui_enabled

        if gui_enabled:
            # initialize pygame
            pygame.init()
            self.clock: pygame.time.Clock = pygame.time.Clock()                     # PyGame Clock to set frame rate
            self.screen: pygame.screen = pygame.display.set_mode((WIDTH, HEIGHT))   # Window where simulation is played
            pygame.display.set_caption("ARS_Robot_Simulation")                      # Window title
            icon = pygame.image.load('images/robot.png')                         # Window icon
            pygame.display.set_icon(icon)
            self.keys: List[Dict[pygame.key, Callable, bool]] = [  # Action keys with relative callback
                dict(key_code=[pygame.K_r], callback=self.reinit_robots, hold=False, pressed=False),
            ]
            self.FONT = pygame.font.SysFont(None, 28)  # Font used for data visualization on top
        else:
            self.pool = ProcessPoolExecutor(os.cpu_count())

        self.environment: Environment = Environment()                               # Environment where the robot is placed
        self.done: bool = False                                                     # Window closed ?
        self.robots: List[Robot] = []
        self.simulation_time = simulation_time
        self.time_left = simulation_time

    def reinit_robots(self):
        robo_amount = len(self.robots)
        self.robots.clear()
        for individual in range(robo_amount):
            self.robots.append(
                Robot(init_pos = self.environment.environment.initial_random_pos, init_rotation = np.random.randint(low=0, high=360), genome = None)
            )

    def set_population(self, population: Population):
        self.time_left = self.simulation_time
        self.robots.clear()
        self.done = False
        for individual in population.individuals:
            self.robots.append(
                Robot(init_pos = self.environment.environment.initial_random_pos, init_rotation = np.random.randint(low=0, high=360), genome = individual)
            )

    def start(self) -> None:

        if self.gui_enabled:
            while not self.done:

                self.get_key_update()
                self.pygame_defaults()

                self.update()
                self.draw()
                self.clock.tick(FPS)
        else:
            futures = []
            environment = self.environment
            for robot in self.robots:
                # self.run_robot_evaluation(self.time_left, robot, environment)
                future = self.pool.submit(self.run_robot_evaluation, self.time_left, robot, environment)
                futures.append(dict(future=future, robot=robot))

            for future in futures:
                future["future"].done()
                future["robot"].genome.fitness = future["future"].result()
            # print("Future Done")

    @staticmethod
    def run_robot_evaluation(generations, robot, environment):
        # print("Run robot evaluation: " + str(robot.genome.genes))
        for i in range(generations):
            robot.update(environment)
        return robot.genome.fitness

    def update(self) -> None:
        for robot in self.robots:
            robot.update(self.environment)

        self.time_left -= 1
        if self.time_left <= 0:
            self.done = True

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.environment.draw(self.screen)
        for robot in self.robots:
            robot.draw(self.screen, pygame)
        self.draw_information(self.screen)
        pygame.display.flip()

    def pygame_defaults(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
                self.stop_callback()

    def get_key_update(self) -> None:
        pressed = pygame.key.get_pressed()
        for key in self.keys:

            is_key_pressed = False

            for key_code in key['key_code']:
                if pressed[key_code]:
                    is_key_pressed = True
                    break

            if is_key_pressed:
                if not key['pressed']:
                    key['callback']()
                    key['pressed'] = not key['hold']
            else:
                key['pressed'] = False

    def draw_information(self, screen):
        self.display_data['frames_left'] = dict(
            display_name = 'Frames Left',
            value = self.time_left
        )

        column_start = 20
        column_width = 200
        row_start = 20
        row_height = 40

        row = 0
        column = 0

        for key, data in self.display_data.items():
            display_name = data['display_name']
            value = data['value']

            screen.blit(
                self.FONT.render(
                    f'{display_name}: {np.round(value, decimals = 3)}',
                    True,
                    COLORS["pink"]),
                (column_start + column * column_width, row_start + row * row_height)
            )

            if row == 1:
                column += 1
                row = 0
            else:
                row += 1
