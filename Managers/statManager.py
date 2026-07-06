# Managers/statManager.py
import threading
import time
import cv2
import numpy as np
from Entities.human import Human
from Managers.logger import Logger
from config import StartValues


class StatManager:
    def __init__(self):
        self.running = False
        self.width = 400
        self.height = 450

    def start_live_stats(self):
        if self.running:
            Logger.log("[StatManager]", "Stat vindue kører allerede")
            return

        self.running = True
        thread = threading.Thread(target=self._live_loop, daemon=True)
        thread.start()
        Logger.log("[StatManager]", "Live-Stats Thread blev startet")

    def _live_loop(self):
        fps_target = 10
        frame_time = 1.0 / fps_target

        while self.running:
            start_time = time.time()

            img = np.zeros((self.height, self.width, 3), dtype=np.uint8)

            try:
                humans = list(Human.humans)
                total_humans = len(humans)
                if total_humans > 0:
                    avg_age = sum(h.age for h in humans) / total_humans
                    avg_energy = sum(h.stats.get("energy", 0) for h in humans) / total_humans
                    avg_nutri = sum(h.stats.get("nutrition", 0) for h in humans) / total_humans
                    avg_money = sum(h.money for h in humans) / total_humans

                    max_gen = max(h.stats.get("generation", 1) for h in humans)

                    states = {}
                    for h in humans:
                        states[h.status] = states.get(h.status, 0) + 1
                else:
                    avg_age = avg_energy = avg_nutri = avg_money = 0
                    max_gen = 1
                    states = {}

                y = 30
                cv2.putText(img, f"Day: {StartValues.daytime}", (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

                y += 30
                cv2.putText(img, f"Total Mennesker: {total_humans}", (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (255, 255, 255), 1)
                y += 30
                cv2.putText(img, f"Hojeste Generation: {max_gen}", (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (100, 255, 100), 1)
                y += 30
                cv2.putText(img, f"Gns. Alder: {avg_age:.1f}", (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200),
                            1)
                y += 30
                cv2.putText(img, f"Gns. Energi: {avg_energy:.1f}", (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            (200, 200, 200), 1)
                y += 30
                cv2.putText(img, f"Gns. Ernaering: {avg_nutri:.1f}", (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            (200, 200, 200), 1)
                y += 30
                cv2.putText(img, f"Gns. Penge: {avg_money:.1f}", (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200),
                            1)

                y += 40
                cv2.putText(img, "Status:", (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1)
                for status, count in states.items():
                    y += 25
                    cv2.putText(img, f"- {status}: {count}", (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

            except Exception:
                pass

            cv2.imshow("Live Simulation Stats", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False
                break

            elapsed = time.time() - start_time
            if elapsed < frame_time:
                time.sleep(frame_time - elapsed)

        try:
            cv2.destroyWindow("Live Simulation Stats")
        except Exception:
            pass