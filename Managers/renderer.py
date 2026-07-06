# Managers/renderer.py
import threading
from PIL import Image, ImageDraw
import os
from datetime import datetime
import time
import cv2
import numpy as np

from Entities.house import House
from Entities.human import Human
from Entities.shop import Shop
from Entities.office import Office
from Managers.logger import Logger
from config import Preview

class Renderer:
    def __init__(self):
        self.width = Preview.picture_width
        self.height = Preview.picture_height
        self.preview_running = False

    def save_snapshot_in_background(self):
        thread = threading.Thread(target=self._draw_and_save, args=(Human.humans, House.houses, Shop.shops, Office.offices))
        thread.start()

    def _draw_and_save(self, humans, houses, shops, offices):
        try:
            img = Image.new("RGB", (self.width, self.height), "white")
            draw = ImageDraw.Draw(img)

            for h in houses.values():
                draw.rectangle([h.x, h.y, h.x2, h.y2], outline="black")

            for s in shops.values():
                draw.rectangle([s.x, s.y, s.x2, s.y2], outline="green")

            for o in offices.values():
                draw.rectangle([o.x, o.y, o.x2, o.y2], outline="orange")

            for m in humans:
                x, y = m.x, m.y
                r = 0.5
                draw.ellipse([x - r, y - r, x + r, y + r], fill="blue")

            folder = "snapshots"
            if not os.path.exists(folder):
                os.makedirs(folder)

            timestamp = datetime.now().strftime("%H-%M-%S")
            filename = f"sim_capture_{timestamp}.png"

            full_path = os.path.join(folder, filename)

            img.save(full_path)
            Logger.log("[Renderer]", f"billede gemt: {filename}")

        except Exception as e:
            Logger.log("[Error]", f"fejl i renderer: {e}")

    def start_live_preview(self):
        if self.preview_running:
            Logger.log("[Renderer]", "preview blev allerede startet")
            return

        self.preview_running = True
        self.live_humans = Human.humans
        self.live_houses = House.houses
        self.live_shops = Shop.shops
        self.live_offices = Office.offices

        thread = threading.Thread(target=self._live_loop, daemon=True)
        thread.start()
        Logger.log("[Renderer]", "Live-Preview Thread blev startet")

    def _live_loop(self):
        fps_target = 30
        frame_time = 1.0 / fps_target

        while self.preview_running:
            start_time = time.time()

            img = Image.new("RGB", (self.width, self.height), "white")
            draw = ImageDraw.Draw(img)

            try:
                for h in self.live_houses.values():
                    draw.rectangle([h.x, h.y, h.x2, h.y2], outline="black")

                for s in self.live_shops.values():
                    draw.rectangle([s.x, s.y, s.x2, s.y2], outline="green")

                for o in self.live_offices.values():
                    draw.rectangle([o.x, o.y, o.x2, o.y2], outline="orange")

                for h in self.live_humans:
                    path = h.stats.get("path", [])
                    if path:
                        draw.line([(h.x, h.y), (path[0][0], path[0][1])], fill="red", width=1)
                        if len(path) > 1:
                            for i in range(len(path)-1):
                                p1 = (path[i][0], path[i][1])
                                p2 = (path[i+1][0], path[i+1][1])
                                draw.line([p1, p2], fill="red", width=1)

                    r = 0.5
                    draw.ellipse([h.x - r, h.y - r, h.x + r, h.y + r], fill="blue")
            except RuntimeError:
                pass

            opencv_image = np.array(img)
            opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_RGB2BGR)

            cv2.imshow("Live Simulation Preview", opencv_image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.preview_running = False
                break

            elapsed = time.time() - start_time
            if elapsed < frame_time:
                time.sleep(frame_time - elapsed)
        cv2.destroyAllWindows()