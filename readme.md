# Autonomous Mapping Car Project

![Project Image](image.png)

## Overview

This project involves building an autonomous mapping car powered by Arduino and Raspberry Pi. The system uses various sensors and components to navigate and create a 2D map of the environment.

## Components

- Arduino
- Raspberry Pi
- Camera
- IR Encoders
- Ultrasonic Sensor
- Compass

## Communication

The communication between Arduino and Raspberry Pi is established via UART. The Raspberry Pi sends commands (e.g., FORWARD, LEFT) to the Arduino, which interprets and executes the corresponding movements. Additionally, the Arduino calculates PWM from the speed measured by IR encoders, sending distance traveled information to the Raspberry Pi every 100ms.

## Obstacle Detection

The project utilizes a camera for a simple edge-finding algorithm to detect obstacles and ground. An ultrasonic sensor, IR encoders on the motors, and a compass are also employed to gather data for navigation.

## Mapping Algorithm

All the collected data is used to create a simple 2D map (top view) of the explored area. The map gradually expands as the car uses an algorithm to find the optimal path.

## How It Works

1. **Command Communication**: aspberry Pi sends movement commands to Arduino via UART (the command will be choosen by "pathfinding algorithm").
2. **Sensor Data Collection**: Camera, ultrasonic sensor, IR encoders, and compass collect data.
3. **Movement Execution**: Arduino interprets commands, calculates PWM, and performs movements.
4. **Distance Tracking**: Arduino sends distance traveled information to Raspberry Pi every 100ms.
5. **Obstacle Detection**: Camera and sensors detect obstacles for navigation.
6. **Mapping Algorithm**: Collected data is used to create a 2D map of the area.

## Future Improvements

- Implement advanced pathfinding algorithms for optimal navigation.
- Enhance obstacle detection algorithms for more complex environments.

