from typing import List, Dict, Callable

import numpy as np
import pygame

from simulator.Constants import WIDTH, HEIGHT
from simulator.Environment import Environment
from simulator.Line import VisualLine
from simulator.Robot import Robot

from simulator import Constants as Const
import time

# Mostly done by Teo
from simulator.Utils import get_pygame_point


class Simulator:

    def __init__(self):
        self.clock: pygame.time.Clock = pygame.time.Clock()  # PyGame Clock to set frame rate
        self.screen: pygame.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Window where simulation is played
        self.environment: Environment = Environment()  # Environment where the robot is placed
        self.done: bool = False  # Window closed ?

        pygame.display.set_caption("ARS_Robot_Simulation")  # Window title
        icon = pygame.image.load('images/robot.png')  # Window icon
        pygame.display.set_icon(icon)
        self.test_mode = False  # For stoping the update for the robot (testing and explaining)

        self.land_marks = []
        for line in self.environment.environment:
            self.land_marks.append(line.start)
            self.land_marks.append(line.end)

        self.compute_relevant_landmarks(Const.START_POS)
        self.robot: Robot = Robot(Const.START_POS, self.relevant_landmarks)  # Robot
        self.estimation_positions = []  # The Z's with the uncertenties

        self.time = time.time()
        self.true_history = [self.robot.pos]
        self.true_history_draw: List[VisualLine] = []

        self.estimated_history = [self.robot.pos]
        self.estimated_history_draw: List[VisualLine] = []
        self.keys: List[Dict[pygame.key, Callable, bool]] = [  # Action keys with relative callback
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

    def start(self) -> None:
        while not self.done:
            self.update()
            self.draw()

            self.clock.tick(60)

    def update(self) -> None:
        self.get_key_update()
        self.get_drag_update()

        self.relevant_landmarks.clear()

        if not self.test_mode:
            self.do_robot_update()

    def draw(self) -> None:
        self.screen.fill(Const.COLORS.light_light_grey)
        self.environment.draw(self.screen)
        self.robot.draw(self.screen)
        self.draw_information(self.screen)

        for viz_line in self.true_history_draw:
            viz_line.draw(self.screen)

        for viz_line in self.estimated_history_draw:
            viz_line.draw(self.screen)

        for relevant_landmark in self.relevant_landmarks:
            viz = VisualLine(self.robot.pos, relevant_landmark, dotted=False, color=Const.COLORS.green)
            viz.draw(self.screen)

        for landmark in self.land_marks:
            pygame.draw.circle(self.screen, Const.COLORS.black, get_pygame_point(landmark), 5)

        for estimated_pos in self.estimation_positions:
            height = 50
            width = 100
            top_left = get_pygame_point(estimated_pos - np.array([width / 2, height / 2]).reshape((2, 1)))
            pygame.draw.ellipse(self.screen, Const.COLORS.blue, pygame.Rect(top_left, (width, height)), 1)

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

        # Go over each landmark and check if its relevant
        self.compute_relevant_landmarks(self.robot.pos)

        self.robot.update(self.environment, self.relevant_landmarks)

        # Take the position after
        end_pos = self.robot.pos

        self.update_history(end_pos, self.true_history, self.true_history_draw, dotted=False, color=Const.COLORS.black)
        self.update_history(
            np.array([self.robot.mu[0, 0], self.robot.mu[1, 0]]).reshape(2, 1),
            self.estimated_history,
            self.estimated_history_draw,
            dotted=True,
            color=Const.COLORS.light_red
        )

        if time.time() - self.time > 5:
            print("New Pos")
            self.time = time.time()
            self.estimation_positions.append(end_pos)

    @staticmethod
    def update_history(end_pos, pos_history, draw_history, dotted: bool, color):
        if np.linalg.norm(pos_history[-1] - end_pos) > Const.UPDATE_DISTANCE:
            vis_line = VisualLine(pos_history[-1], end_pos, dotted=dotted, color=color)
            pos_history.append(end_pos)
            draw_history.append(vis_line)

    def draw_information(self, screen: pygame.display) -> None:
        font_color = Const.COLORS.black
        screen.blit(Const.FONT.render(f'theta: {np.round(np.rad2deg(self.robot.theta), decimals=3)}', True, font_color),
                    (20, 20))
        screen.blit(Const.FONT.render(f'v_l: {self.robot.v_l}', True, font_color), (20, 40))
        screen.blit(Const.FONT.render(f'v_r: {self.robot.v_r}', True, font_color), (20, 60))
        screen.blit(Const.FONT.render(f'pos_x: {np.round(self.robot.pos[0].item(), decimals=3)}', True, font_color),
                    (180, 20))
        screen.blit(Const.FONT.render(f'pos_y: {np.round(self.robot.pos[1].item(), decimals=3)}', True, font_color),
                    (180, 40))

    def compute_relevant_landmarks(self, pos):
        self.relevant_landmarks = []
        for land_mark in self.land_marks:
            if np.linalg.norm(pos - land_mark) < Const.LANDMARK_DIST:
                self.relevant_landmarks.append(land_mark)
