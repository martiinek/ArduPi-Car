#motion.py

import tkinter as tk
import math
from enum import Enum
import time

commands = ["STOP", "FRWD", "BKWD", "LEFT", "RIHT"]

class Commands(Enum):
    STOP = 0
    FRWD = 1
    BKWD = 2
    LEFT = 3
    RIHT = 4

class MotionController:
    def __init__(self):
        self.width, self.height = 1000, 1000
        self.angle_line_startx = self.width / 2
        self.angle_line_starty = self.height / 2
        self.angle = 0
        self.mileage = 0
        self.line_length = 20
        self.size_factor = 0.2
        self.x_factor = self.width / 2
        self.y_factor = self.height / 2
        self.x_transform_offset = 0
        self.y_transform_offset = 0
        self.x_rot_offset = 0
        self.y_rot_offset = 0
        self.turn = False
        self.cmd_pick = 0
        self.polygon_points = []
        
        self.root = tk.Tk()
        self.root.title("Map")
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

    def arr_pos(self, x, y):
        image_width = 640 * self.size_factor
        image_height = 480 * self.size_factor
        
        self.x_rot_offset = self.x_factor - image_width / 2
        self.y_rot_offset = self.y_factor - image_height / 2
        angle_in_rad_rot = (self.angle + 90) * math.pi / 180
        cos_theta = math.cos(angle_in_rad_rot)
        sin_theta = math.sin(angle_in_rad_rot)

        x_rot = self.size_factor * (x - self.x_factor) * cos_theta - self.size_factor * (y - self.y_factor) * sin_theta + self.x_rot_offset
        y_rot = self.size_factor * (x - self.x_factor) * sin_theta + self.size_factor * (y - self.y_factor) * cos_theta + self.y_rot_offset

        angle_in_rad_transform = self.angle * math.pi / 180
        cos_fi = math.cos(angle_in_rad_transform)
        sin_fi = math.sin(angle_in_rad_transform)
        self.x_transform_offset = self.mileage * self.size_factor * cos_fi
        self.y_transform_offset = self.mileage * self.size_factor * sin_fi
        
        x_transformed = x_rot + self.x_transform_offset
        y_transformed = y_rot + self.y_transform_offset

        return x_transformed, y_transformed


    def gen_map(self, surrounding, distance, angle, mileage):
        self.angle = angle
        self.mileage = mileage
        angle_in_rad = self.angle * math.pi / 180
        cos_theta = math.cos(angle_in_rad)
        sin_theta = math.sin(angle_in_rad)
        connection_points = [(0, 0),(0, 0)]

        angle_line_endx = self.angle_line_startx + self.line_length * cos_theta
        angle_line_endy = self.angle_line_starty + self.line_length * sin_theta

        self.canvas.delete("angle_line")
        self.canvas.create_line(self.angle_line_startx, self.angle_line_starty, angle_line_endx, angle_line_endy, fill="red", tags="angle_line")

        #if mileage % 200 == 0:
        #   self.turn = True
            
        if self.turn == True:
            x_start_rot, y_start_rot = self.arr_pos(surrounding[0][0], surrounding[0][1])
            x_end_rot, y_end_rot = self.arr_pos(surrounding[len(surrounding)-2][0], surrounding[len(surrounding)-2][1])

            self.x_factor = (x_start_rot + x_end_rot) / 2
            self.y_factor = (y_start_rot + y_end_rot) / 2
            self.turn = False
        
        self.polygon_points = []
        self.polygon_points = [self.arr_pos(x, y) for x, y in surrounding]
        self.canvas.create_polygon(self.polygon_points, outline="white", fill="white", tags="map_polygon")
        
        if distance < 30:
            self.cmd_pick = Commands.STOP.value
        else: self.cmd_pick = Commands.FRWD.value
            
        direction = commands[self.cmd_pick]
        self.root.update()
        return direction

