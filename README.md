# Solar-System-Simulator

## Abstract
This repository presents a real-time three-dimensional simulation of the solar system implemented in Python using OpenGL. The project models the Sun, the major planets, orbital motion, and selected visual phenomena such as the Earth–Moon system and Saturn’s ring. 

## Objectives
- Provide an accessible and visually coherent simulation of planetary motion.
- Demonstrate core concepts in computer graphics, including rendering, transformations, and scene organization.
- Support further extension for additional celestial bodies, physical parameters, and interactive features.

## Features
- Real-time rendering of the Sun and eight principal planets.
- Time-driven orbital and rotational motion.
- A structured hierarchical model of celestial objects.
- Visual enhancements including ring and asteroid-belt effects.
- Keyboard and mouse interaction for navigation and exploration.
- A modular codebase separated into rendering, simulation, control, and model components.

## Requirements
- Python 3.x
- PyOpenGL
- PyOpenGL-accelerate

## Installation
```bash
pip install PyOpenGL PyOpenGL-accelerate
python main.py
```

## Project Structure
- main.py: application entry point.
- models/: definitions for planets, moons, and the solar system scene.
- core/: rendering, window management, and simulation timing.
- control/: keyboard and mouse input handling.
- effect/: visual effects such as stars, rings, and asteroid belts.
- ui/: HUD and text-rendering components.