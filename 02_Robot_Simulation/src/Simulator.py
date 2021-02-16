import numpy as np
import pygame

from src.Constants import width, height
from src.Environment import Environment
from src.Robot import Robot

import Constants as Const


class Simulator:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((width, height))
        self.environment = Environment()
        self.robot = Robot(Const.start_pos)
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
        self.done = False
        pygame.display.set_caption("ARS_Robot_Simulation")
        icon = pygame.image.load('images/robot.png')
        pygame.display.set_icon(icon)

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
        self.draw_information(self.screen)
        pygame.display.flip()

    def get_key_update(self):
        pressed = pygame.key.get_pressed()
        for key in self.keys:
            for key_code in key['key_code']:
                if pressed[key_code]:
                    if not key['pressed']:
                        key['callback']()
                #         key['pressed'] = True
                # else:
                #     key['pressed'] = False

    def pygame_defaults(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

    def do_robot_update(self):
        self.robot.update(self.environment)

    def draw_information(self, screen):
        screen.blit(Const.font.render(f'theta: {np.round(np.rad2deg(self.robot.theta), decimals=3)}', True, Const.colors["pink"]), (20, 20))
        screen.blit(Const.font.render(f'v_l: {self.robot.v_l}', True, Const.colors["pink"]), (20, 40))
        screen.blit(Const.font.render(f'v_r: {self.robot.v_r}', True, Const.colors["pink"]), (20, 60))
        screen.blit(Const.font.render(f'pos_x: {np.round(self.robot.pos[0].item(), decimals=3)}', True, Const.colors["pink"]), (180, 20))
        screen.blit(Const.font.render(f'pos_y: {np.round(self.robot.pos[1].item(), decimals=3)}', True, Const.colors["pink"]), (180, 40))
