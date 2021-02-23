import numpy as np
import pygame

from src.Constants import WIDTH, HEIGHT
from src.Environment import Environment
from src.Population import Population
from src.Robot import Robot

import Constants as Const


class Simulator:

    def __init__(self):
        self.clock: pygame.time.Clock = pygame.time.Clock()  # PyGame Clock to set frame rate
        self.screen: pygame.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Window where simulation is played
        self.environment: Environment = Environment()  # Environment where the robot is placed
        self.done: bool = False  # Window closed ?
        pygame.display.set_caption("ARS_Robot_Simulation")  # Window title
        icon = pygame.image.load('images/robot.png')  # Window icon
        pygame.display.set_icon(icon)
        self.population = Population()
        self.frame_to_death = Const.LIFES_STEPS

    def start(self) -> None:
        while not self.done:
            self.pygame_defaults()

            self.update()
            self.draw()

            self.clock.tick(Const.FPS)

    def update(self) -> None:
        if self.frame_to_death > 0:
            self.population.update(self.environment, Const.LIFES_STEPS - self.frame_to_death)
            self.frame_to_death -= 1
        else:
            self.population.generation_cycle()
            self.frame_to_death = Const.LIFES_STEPS

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.environment.draw(self.screen)
        self.population.draw(self.screen)
        self.draw_information(self.screen)
        pygame.display.flip()

    def pygame_defaults(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

    def draw_information(self, screen):
        screen.blit(
            Const.FONT.render(
                f'Generation: {self.population.generation + 1}',
                True,
                Const.COLORS["pink"]),
            (20, 20)
        )
        screen.blit(
            Const.FONT.render(
                f'Frames Left: {self.frame_to_death}',
                True,
                Const.COLORS["pink"]),
            (20, 40)
        )
        screen.blit(
            Const.FONT.render(
                f'AVG Fitness: {np.round(self.population.avg_fitness[self.population.generation], decimals=3)}',
                True,
                Const.COLORS["pink"]),
            (175, 20)
        )
        screen.blit(
            Const.FONT.render(
                f'Best Fitness: {np.round(self.population.best_fitness[self.population.generation], decimals=3)}',
                True,
                Const.COLORS["pink"]),
            (175, 40)
        )
