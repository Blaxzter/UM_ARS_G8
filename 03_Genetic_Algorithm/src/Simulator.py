import numpy as np
import pygame

from src.Constants import width, height
from src.Environment import Environment
from src.Population import Population
from src.Robot import Robot

import Constants as Const


class Simulator:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((width, height))
        self.environment = Environment()
        self.robot = Robot(Const.start_location)
        self.population = Population()
        self.keys = [
            dict(key_code=[pygame.K_KP7], callback=self.robot.increase_left, pressed=False),
            dict(key_code=[pygame.K_KP4], callback=self.robot.decrease_left, pressed=False),
            dict(key_code=[pygame.K_KP9], callback=self.robot.increase_right, pressed=False),
            dict(key_code=[pygame.K_KP6], callback=self.robot.decrease_right, pressed=False),
            dict(key_code=[pygame.K_w, pygame.K_KP8], callback=self.robot.increase_both, pressed=False),
            dict(key_code=[pygame.K_s, pygame.K_KP5], callback=self.robot.decrease_both, pressed=False),
            dict(key_code=[pygame.K_x], callback=self.robot.stop, pressed=False),
            dict(key_code=[pygame.K_a], callback=self.robot.rotate_left, pressed=False),
            dict(key_code=[pygame.K_d], callback=self.robot.rotate_right, pressed=False),
            dict(key_code=[pygame.K_KP_MULTIPLY], callback=self.robot.hide_sensor, pressed=False),
            dict(key_code=[pygame.K_KP_MINUS], callback=self.robot.show_sensor, pressed=False)
        ]
        self.frame_to_death = Const.individuals_life_steps
        self.done = False
        pygame.display.set_caption("ARS_Robot_Simulation")
        icon = pygame.image.load('images/robot.png')
        pygame.display.set_icon(icon)

    def start(self):
        while not self.done:
            self.pygame_defaults()

            self.update()
            self.draw()

            self.clock.tick(1200)

    def update(self):
        if self.frame_to_death > 0:
            self.population.update(self.environment, Const.individuals_life_steps - self.frame_to_death)
            self.frame_to_death -= 1
        else:
            self.population.generation_cycle()
            self.frame_to_death = Const.individuals_life_steps

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
            Const.font.render(f'Generation: {self.population.generation + 1}', True, Const.colors["pink"]), (20, 20)
        )
        screen.blit(
            Const.font.render(f'Frames Left: {self.frame_to_death}', True, Const.colors["pink"]), (20, 40)
        )
        screen.blit(
            Const.font.render(f'AVG Fitness: {np.round(self.population.avg_fitness[self.population.generation], decimals=3)}', True, Const.colors["pink"]), (175, 20)
        )
        screen.blit(
            Const.font.render(f'Best Fitness: {np.round(self.population.best_fitness[self.population.generation], decimals=3)}', True, Const.colors["pink"]), (175, 40)
        )