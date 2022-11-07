import _thread
from random import getrandbits
from lib import colorsys
from lib.queue import Queue

try:
    from machine import Pin
    import uasyncio as asyncio
    import mutex
    import neopixel
    import utime as time
except:
    from moc.machine import Pin
    import asyncio
    import time


class LedService:
    active_task = None
    loop = None
    queue = Queue()

    def __init__(self):
        self.led = Led()
        t = _thread.start_new_thread(target=self.__looper, daemon=True)
        t.start()

    def __looper(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.__handler())

    async def __handler(self):
        while True:
            task = self.queue.get()
            await task

    def set_color(self, hue):
        self.__kill_tasks()
        task = self.loop.create_task(self.led.set_color(hue))
        self.queue.put(task)

    def set_brightness(self, light):
        pass

    def demo(self):
        self.__kill_tasks()
        task = self.loop.create_task(self.led.demo())
        self.queue.put(task)

    def off(self):
        self.__kill_tasks()
        task = self.loop.create_task(self.led.off())
        self.queue.put(task)

    def __kill_tasks(self):
        if self.active_task is None:
            return

        self.active_task.cancel()


class Led:
    color = (100, 100, 100)
    mutex = mutex.Mutex()
    np = neopixel.NeoPixel(Pin(0), 144)

    def off(self):
        return self.__fade(0, 0, 0)

    def set_color(self, hue):
        h, l, s = colorsys.rgb_to_hls(self.color[0], self.color[1], self.color[2])
        r, g, b = colorsys.hls_to_rgb(hue, l, s)
        return self.__fade(r, g, b)

    def set_brightness(self, light):
        h, l, s = self.current_hls()
        r, g, b = colorsys.hls_to_rgb(h, light, s)
        return self.__fade(r, g, b)

    async def demo(self):
        l = 30
        while True:
            h = self.__random_range(0, 360)
            s = self.__random_range(70, 80)
            color = colorsys.hls_to_rgb(h, l, s)
            await self.__fade(color[0], color[1], color[2], max_steps=255, sleep_time=self.__random_range(0.3, 0.5))
            delay = self.__random_range(7, 12)
            await asyncio.sleep(delay)

    async def __fade(self, r, g, b, max_steps=50, sleep_time=None):
        diff = [0] * 3
        diff[0] = self.color[0] - r
        diff[1] = self.color[1] - g
        diff[2] = self.color[2] - b
        n_steps = self.__calc_steps(max_steps, diff)

        for i in range(0, 3):
            diff[i] = int(diff[i] / n_steps)

        for i in range(0, n_steps):
            self.color = (self.color[0] - diff[0], self.color[1] - diff[1], self.color[2] - diff[2])
            self.np.fill(self.color)
            self.np.write()
            if sleep_time is not None:
                await asyncio.sleep(sleep_time)

        self.color = (r, g, b)
        self.np.fill(self.color)
        self.np.write()

    def current_hls(self):
        return colorsys.rgb_to_hls(self.color[0], self.color[1], self.color[2])

    @staticmethod
    def __calc_steps(max_steps, diff):
        highest_diff = max(abs(i) for i in diff)
        return min([highest_diff, max_steps])

    @staticmethod
    def __random_range(i, j):
        b = getrandbits(16)
        diff = abs(j - i)
        ration = b / 65535
        return i + int(diff * ration)
