import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.solar_system import SolarSystem
from core.renderer import Renderer
from core.window import start_main_loop

def main():
    print("🚀 Starting Solar System Simulation...")
    
    solar_system_instance = SolarSystem()
    renderer_instance = Renderer()

    start_main_loop(solar_system_instance, renderer_instance)

if __name__ == '__main__':
    main()