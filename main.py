import time

from Managers.renderer import Renderer
from Managers.saveSimulation import Saver
from Managers.simulationLoop import Loop
from Managers.logger import Logger
from Managers.statManager import StatManager

from config import Preview
from Managers.name_manager import NameManager

def start_simulation():
    Logger.log("[Main]", "Starter simulation")

    NameManager.load_names()
    Loop.start()

    renderer = Renderer()
    stat_manager = StatManager()

    last_picture_time = time.time()

    if Preview.live_preview: renderer.start_live_preview()
    if Preview.live_stats: stat_manager.start_live_stats()

    try:
        while True:
            Loop.tick()

            time.sleep(0.016)

            if Preview.generate_picture > 0:
                current_time = time.time()
                if current_time - last_picture_time >= (Preview.generate_picture * 60):
                    Logger.log("[Main]", "Tager billede")
                    renderer.save_snapshot_in_background()
                    last_picture_time = current_time

    except KeyboardInterrupt:
        Logger.log("[Main]", "Simulation stoppet af bruger")
        Saver.save()

    finally:
        if Preview.live_preview: renderer.preview_running = False
        if Preview.live_stats: stat_manager.running = False

if __name__ == '__main__':
    start_simulation()