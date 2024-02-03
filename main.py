# main.py

import view
import serial_bus
import compass
from motion import MotionController
import tcp
from gpiozero import CPUTemperature

def main():
    motion_controller = MotionController()
    while True:
        cpu = CPUTemperature()
        print(cpu)
        surrounding = view.check_ground()
        distance = view.ping()
        angle = compass.get_angle()
        mileage = serial_bus.read()
        direction = motion_controller.gen_map(surrounding, distance, angle, mileage)
        serial_bus.write("STOP")
        
if __name__ == "__main__":
    main()
