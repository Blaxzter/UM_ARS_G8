from typing import List, Dict, Callable

import numpy as np
import pygame

from src.Constants import WIDTH, HEIGHT
from src.Environment import Environment
from src.Robot import Robot

import Constants as Const

# Mostly done by Teo

class Simulator:

    def __init__(self):
        self.clock: pygame.time.Clock = pygame.time.Clock()                     # PyGame Clock to set frame rate
        self.screen: pygame.screen = pygame.display.set_mode((WIDTH, HEIGHT))   # Window where simulation is played
        self.environment: Environment = Environment()                           # Environment where the robot is placed
        self.robot: Robot = Robot(Const.START_POS)                              # Robot
        self.keys: List[Dict[pygame.key, Callable, bool]] = [                   # Action keys with relative callback
            dict(key_code=[pygame.K_KP7], callback=self.robot.increase_left, hold=False, pressed=False),
            dict(key_code=[pygame.K_KP4], callback=self.robot.decrease_left, hold=False, pressed=False),
            dict(key_code=[pygame.K_KP9], callback=self.robot.increase_right, hold=False, pressed=False),
            dict(key_code=[pygame.K_KP6], callback=self.robot.decrease_right, hold=False, pressed=False),
            dict(key_code=[pygame.K_KP8], callback=self.robot.increase_both, hold=False, pressed=False),
            dict(key_code=[pygame.K_KP5], callback=self.robot.decrease_both, hold=False, pressed=False),
            dict(key_code=[pygame.K_w], callback=self.robot.increase_both, hold=True, pressed=False),
            dict(key_code=[pygame.K_s], callback=self.robot.decrease_both, hold=True, pressed=False),
            dict(key_code=[pygame.K_x, pygame.K_r], callback=self.robot.stop, hold=False, pressed=False),
            dict(key_code=[pygame.K_a], callback=self.robot.rotate_left, hold=True, pressed=False),
            dict(key_code=[pygame.K_d], callback=self.robot.rotate_right, hold=True, pressed=False),
            dict(key_code=[pygame.K_KP_MULTIPLY], callback=self.robot.toggle_sensor, hold=False, pressed=False),
            dict(key_code=[pygame.K_m], callback=self.toggle_test_mode, hold=False, pressed=False),
            dict(key_code=[pygame.K_n], callback=self.do_robot_update, hold=False, pressed=False)
        ]

        self.done: bool = False                                                 # Window closed ?
        pygame.display.set_caption("ARS_Robot_Simulation")                      # Window title
        icon = pygame.image.load('images/robot.png')                            # Window icon
        pygame.display.set_icon(icon)
        self.test_mode = False

    def start(self) -> None:
        while not self.done:

            self.update()
            self.draw()

            self.clock.tick(60)

    def update(self) -> None:
        self.get_key_update()
        self.get_drag_update()
        if not self.test_mode:
            self.do_robot_update()

    def draw(self) -> None:
        self.screen.fill((0, 0, 0))
        self.environment.draw(self.screen)
        self.robot.draw(self.screen)
        self.draw_information(self.screen)
        pygame.display.flip()

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


    def get_drag_update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.robot.dragging = True
                    mouse_x, mouse_y = event.pos
                    self.robot.drag(mouse_x, mouse_y)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.robot.dragging = False

            elif event.type == pygame.MOUSEMOTION:
                if self.robot.dragging:
                    mouse_x, mouse_y = event.pos
                    self.robot.drag(mouse_x, mouse_y)

    def toggle_test_mode(self):
        self.test_mode = not self.test_mode

    def do_robot_update(self) -> None:
        self.robot.update(self.environment)

    def draw_information(self, screen: pygame.display) -> None:
        font_color = Const.COLORS["white"]
        screen.blit(Const.FONT.render(f'theta: {np.round(np.rad2deg(self.robot.theta), decimals=3)}', True, font_color), (20, 20))
        screen.blit(Const.FONT.render(f'v_l: {self.robot.v_l}', True, font_color), (20, 40))
        screen.blit(Const.FONT.render(f'v_r: {self.robot.v_r}', True, font_color), (20, 60))
        screen.blit(Const.FONT.render(f'pos_x: {np.round(self.robot.pos[0].item(), decimals=3)}', True, font_color), (180, 20))
        screen.blit(Const.FONT.render(f'pos_y: {np.round(self.robot.pos[1].item(), decimals=3)}', True, font_color), (180, 40))
