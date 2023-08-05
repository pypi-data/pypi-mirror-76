import pyautogui
from time import sleep

from threading import Thread, Event


class MouseJiggler(Thread):
    def __init__(self, idle_time=5, sleep_time=0.1, jiggle=1,
                 ignore_idle=False, daemonic=False):
        super().__init__()
        self.stop_event = Event()
        self.jiggle_x = jiggle
        self.jiggle_y = jiggle
        self.ignore_idle = ignore_idle
        self.idle_time = idle_time
        self.sleep_time = sleep_time
        self.last_move = 0
        self.last_pos = pyautogui.position()
        self.idle = False
        if daemonic:
            self.setDaemon(True)

    @staticmethod
    def on_mouse_move(mouse_position):
        pass

    @staticmethod
    def on_jiggle():
        pass

    @staticmethod
    def on_idle():
        pass

    @staticmethod
    def on_active():
        pass

    @staticmethod
    def on_stop():
        pass

    def run(self):
        while not self.stop_event.is_set():
            mousepos = pyautogui.position()
            if mousepos != self.last_pos:
                self.last_pos = mousepos
                self.last_move = 0
                if self.idle:
                    self.on_active()
                else:
                    self.on_mouse_move(mousepos)
                self.idle = False

            if not self.idle and self.last_move >= self.idle_time:
                self.on_idle()
                self.idle = True

            if self.idle or self.ignore_idle:
                self.on_jiggle()
                self.last_move = 0
                pyautogui.moveTo(mousepos.x + self.jiggle_x,
                                 mousepos.y + self.jiggle_y)
                pyautogui.moveTo(mousepos.x - self.jiggle_x,
                                 mousepos.y - self.jiggle_y)
                pyautogui.moveTo(mousepos.x + self.jiggle_x,
                                 mousepos.y - self.jiggle_y)
                pyautogui.moveTo(mousepos.x - self.jiggle_x,
                                 mousepos.y + self.jiggle_y)
                pyautogui.moveTo(mousepos.x,
                                 mousepos.y)

            sleep(self.sleep_time)
            self.last_move += self.sleep_time

        self.on_stop()

    def stop(self):
        self.stop_event.set()

