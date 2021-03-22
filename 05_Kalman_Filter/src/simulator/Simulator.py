import math
from typing import List, Dict, Callable

import numpy as np
import pygame

from simulator.Constants import WIDTH, HEIGHT, EPSILON
from simulator.Environment import Environment
from simulator.Line import VisualLine
from simulator.Robot import Robot, rotate

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

        self.relevant_landmarks = []
        self.land_marks = []
        for line in self.environment.environment:

            for point in [line.start, line.end]:

                closest = math.inf
                for added_landmark in self.land_marks:
                    dist = np.linalg.norm(point - added_landmark)
                    if dist < closest:
                        closest = dist

                if closest > EPSILON:
                    self.land_marks.append(point)

        self.robot: Robot = Robot(Const.START_POS)  # Robot
        self.compute_relevant_landmarks()

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
            dict(key_code=[pygame.K_SPACE], callback=self.toggle_test_mode, hold=False, pressed=False),
            dict(key_code=[pygame.K_n], callback=self.do_robot_update, hold=False, pressed=False),

            dict(key_code=[pygame.K_KP_PLUS], callback=self.add_sensor_noise, hold=True, pressed=False),
            dict(key_code=[pygame.K_KP_MINUS], callback=self.remove_sensor_noise, hold=True, pressed=False),

            dict(key_code=[pygame.K_UP], callback=self.add_bearing_noise, hold=True, pressed=False),
            dict(key_code=[pygame.K_DOWN], callback=self.remove_bearing_noise, hold=True, pressed=False),

            dict(key_code=[pygame.K_LEFT], callback=self.add_motion_noise_l, hold=True, pressed=False),
            dict(key_code=[pygame.K_RIGHT], callback=self.remove_motion_noise_l, hold=True, pressed=False),

            dict(key_code=[pygame.K_DELETE], callback=self.add_motion_noise_r, hold=True, pressed=False),
            dict(key_code=[pygame.K_END], callback=self.remove_motion_noise_r, hold=True, pressed=False),
        ]

        self.updated = False

    def start(self) -> None:
        while not self.done:
            self.update()
            self.draw()

            self.clock.tick(60)

    def update(self) -> None:
        self.get_key_update()
        self.get_drag_update()

        if not self.test_mode:
            self.relevant_landmarks.clear()
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
            pos_ = relevant_landmark['pos']
            viz = VisualLine(self.robot.pos, pos_, dotted=False, color=Const.COLORS.green)
            viz.draw(self.screen)

            pos_1 = pos_ + 20

            pos_2 = np.array(pos_1)
            pos_2[1] += 20

            pos_3 = np.array(pos_2)
            pos_3[1] += 20

            self.screen.blit(Const.LANDMARK_FONT.render(f'relativ bearing: {np.round(np.rad2deg(relevant_landmark["bearing"]), decimals = 3)}', True, Const.COLORS.black), get_pygame_point(pos_1))
            self.screen.blit(Const.LANDMARK_FONT.render(f'abs bearing    : {np.round(np.rad2deg(relevant_landmark["orientation"]), decimals = 3)}', True, Const.COLORS.black), get_pygame_point(pos_2))

            self.screen.blit(Const.LANDMARK_FONT.render(f'Calc Theta: {np.round(relevant_landmark["calc_theta"], decimals = 3)}', True, Const.COLORS.black), get_pygame_point(pos_3))

        for landmark in self.land_marks:
            pygame.draw.circle(self.screen, Const.COLORS.black, get_pygame_point(landmark), 5)

        height = np.abs(self.robot.sigma[1, 1])
        width = np.abs(self.robot.sigma[0, 0])
        center_pos = pygame.Vector2(self.robot.mu[0, 0] - width / 2, self.robot.mu[1, 0] - height / 2)
        pygame.draw.ellipse(self.screen, Const.COLORS.blue, pygame.Rect(center_pos, (width, height)), 1)
        ratio = height/width

        if time.time() - self.time > 5:
            self.time = time.time()
            self.estimation_positions.append({
                'pos': center_pos,
                'height': height,
                'width': width
            })

        for estimated_pos in self.estimation_positions:
            pos = estimated_pos['pos']
            c_height = estimated_pos['height']
            c_width = estimated_pos['width']
            pygame.draw.ellipse(self.screen, Const.COLORS.blue, pygame.Rect(pos, (c_width, c_height)), 1)

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
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if event.button == 1:
            #         self.robot.dragging = True
            #         mouse_x, mouse_y = event.pos
            #         self.robot.drag(mouse_x, mouse_y)
            #
            # elif event.type == pygame.MOUSEBUTTONUP:
            #     if event.button == 1:
            #         self.robot.dragging = False
            #
            # elif event.type == pygame.MOUSEMOTION:
            #     if self.robot.dragging:
            #         mouse_x, mouse_y = event.pos
            #         self.robot.drag(mouse_x, mouse_y)

    def toggle_test_mode(self):
        self.test_mode = not self.test_mode

    def do_robot_update(self) -> None:

        # Go over each landmark and check if its relevant
        self.compute_relevant_landmarks()

        self.robot.update(self.environment, self.relevant_landmarks)

        # Take the position after
        end_pos = self.robot.pos

        # Change colors for update drawing
        if len(self.relevant_landmarks) >= 3:
            self.updated += 1

        if len(self.relevant_landmarks) < 3:
            self.updated = 0

        self.update_history(end_pos, self.true_history, self.true_history_draw, dotted=False, color=Const.COLORS.black)
        self.update_history(
            np.array([self.robot.mu[0, 0], self.robot.mu[1, 0]]).reshape(2, 1),
            self.estimated_history,
            self.estimated_history_draw,
            dotted=True,
            color=Const.COLORS.grey if self.updated == 1 else Const.COLORS.light_red
        )

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

        screen.blit(Const.FONT.render(f'mu[3]: {np.round(np.rad2deg(self.robot.mu[2].item()), decimals=3)}', True, font_color), (180, 60))
        screen.blit(Const.FONT.render(f'theta: {np.round(np.rad2deg(self.robot.theta%(2*np.pi)), decimals=3)}', True, font_color), (340, 60))
        screen.blit(Const.FONT.render(f'triag : {np.round(np.rad2deg(self.robot.detected_theta), decimals=3)}', True, font_color), (540, 60))
        screen.blit(Const.FONT.render(f'diff : {np.round(np.abs(np.rad2deg(self.robot.detected_theta) - np.rad2deg(self.robot.theta%(2*np.pi))), decimals=3)}', True, font_color), (540, 40))

        screen.blit(Const.FONT.render(f'Sensor Noise : {np.round(Const.sensor_noise, decimals=3)}', True, font_color), (740, 20))
        screen.blit(Const.FONT.render(f'Bearing Noise : {np.round(Const.bearing_noise, decimals=3)}', True, font_color), (740, 40))
        screen.blit(Const.FONT.render(f'Motion Noise L: {np.round(Const.motion_noise_l, decimals=3)}', True, font_color), (740, 60))
        screen.blit(Const.FONT.render(f'Motion Noise R: {np.round(Const.motion_noise_r, decimals=3)}', True, font_color), (940, 60))

    def compute_relevant_landmarks(self):
        self.relevant_landmarks.clear()
        for land_mark in self.land_marks:
            landmark_deg = land_mark - self.robot.pos
            distance = np.linalg.norm(landmark_deg)
            if distance < Const.LANDMARK_DIST:
                relative_position = landmark_deg / distance

                abs_bearing = (2 * np.pi - math.atan2(relative_position[1], -relative_position[0])) % (2 * np.pi)
                relative_bearing = (math.atan2(relative_position[1], relative_position[0]) - (2 * np.pi - self.robot.theta)) % (2 * np.pi)

                self.relevant_landmarks.append(dict(
                    pos=land_mark,
                    dist=distance + np.random.normal() * Const.sensor_noise,
                    bearing = relative_bearing,
                    orientation = abs_bearing,
                    calc_theta = np.rad2deg(self.robot.theta + np.random.normal() * Const.bearing_noise) % 360
                ))

    def add_sensor_noise(self):
        Const.sensor_noise += 0.01

    def remove_sensor_noise(self):
        if Const.sensor_noise - 0.01 >= 0:
            Const.sensor_noise -= 0.01

    def add_bearing_noise(self):
        Const.bearing_noise += 0.01

    def remove_bearing_noise(self):
        if Const.bearing_noise - 0.01 >= 0:
            Const.bearing_noise -= 0.01

    def add_motion_noise_l(self):
        Const.motion_noise_l += 0.01

    def remove_motion_noise_l(self):
        if Const.motion_noise_l - 0.01 >= 0:
            Const.motion_noise_l -= 0.01

    def add_motion_noise_r(self):
        Const.motion_noise_r += 0.01

    def remove_motion_noise_r(self):
        if Const.motion_noise_r - 0.01 >= 0:
            Const.motion_noise_r -= 0.01
